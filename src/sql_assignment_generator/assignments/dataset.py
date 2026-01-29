from collections.abc import Sequence
from dataclasses import dataclass
import dav_tools
import sqlglot
from sqlscope import Catalog, build_catalog_from_sql

from ..constraints.schema import SchemaConstraint
from .. import llm
from ..constraints import SchemaConstraint, schema as schema_constraints
from ..exceptions import SQLParsingError, ConstraintValidationError


@dataclass
class Dataset:
    '''A SQL dataset related to a specific domain, including schema creation and data insertion commands.'''

    create_commands: list[str]
    '''SQL commands to create the database schema.'''

    insert_commands: list[str]
    '''SQL commands to insert data into the database.'''

    domain: str
    '''The domain associated with the dataset.'''

    _catalog_cache: Catalog | None = None
    '''Cached SQLScope Catalog for the dataset.'''

    _catalog_cache_commands_hash: int | None = None
    '''Hash of the CREATE TABLE commands used to build the cached Catalog.'''

    @property
    def catalog(self) -> Catalog:
        '''
        Build and return a SQLScope Catalog from the dataset's SQL commands.
        The result is cached for handling multiple accesses efficiently.
        Cache is properly invalidated if the CREATE TABLE commands change.
        '''
        if self._catalog_cache is None or self._catalog_cache_commands_hash != hash(tuple(self.create_commands)):
            full_sql = '\n'.join(self.create_commands)
            self._catalog_cache = build_catalog_from_sql(full_sql)
            self._catalog_cache_commands_hash = hash(tuple(self.create_commands))
        
        return self._catalog_cache
    
    def to_sql_no_context(self) -> str:
        '''Generate the SQL commands to create and populate the dataset without schema context.'''

        create_cmds = '\n'.join(self.create_commands)
        insert_cmds = '\n'.join(self.insert_commands)

        return f'''{create_cmds}\n\n{insert_cmds}'''

    def to_sql(self, schema: str) -> str:
        '''Generate the SQL commands to create and populate the dataset within the specified schema.'''

        # Normalize schema name
        schema = schema.lower().replace(' ', '_')

        create_cmds = '\n\n'.join(self.create_commands)
        insert_cmds = '\n\n'.join(self.insert_commands)

        return f'''BEGIN;

DROP SCHEMA IF EXISTS {schema} CASCADE;
CREATE SCHEMA {schema};
SET search_path TO {schema};

{create_cmds}

{insert_cmds}

COMMIT;'''
    
    @staticmethod
    def generate(domain: str,
                 constraints: Sequence[SchemaConstraint],
                 extra_details: list[str] = [],
                 *,
                 max_attempts: int = 5
        ) -> 'Dataset':
        '''Generate a SQL dataset based on the specified parameters.'''

        # merge similar constraints
        constraints = schema_constraints.merge_constraints(constraints)

        formatted_constraints = '\n'.join(f'- {c.description}' for c in constraints)

        # remove empty extra details        
        extra_details = [detail for detail in extra_details if detail.strip() != '']
        # dataset characteristics str
        if len(extra_details) > 0:
            extra_details_str = "The dataset must have the following characteristics:\n"
            for detail in extra_details:
                extra_details_str += f"- {detail}\n"
        else:
            extra_details_str = ''
        
        prompt_text = f'''
Generate a SQL dataset about the following domain: "{domain}".
{extra_details_str}

MANDATORY CONSTRAINTS:
- FOREIGN KEY attributes should have the REFERENCES keyword inline (e.g. "col TYPE REFERENCES table_name(column_name)").
{formatted_constraints}

MANDATORY OUTPUT (JSON):
{{
    "schema_tables": ["CREATE TABLE t1(...);", "CREATE TABLE t2(...);"],
    "insert_commands": ["INSERT INTO t1...", "INSERT INTO t2..."]
}}

INSERT INTO statements must have following format (Multi-row insert): 
INSERT INTO tableName(<all columns except SERIAL/AUTO_INCREMENT>) VALUES 
    (val_1, val_2, ...),
    (val_n, val_n+1, ...);

For each table, insert at least 5 rows of data.
Skip any SERIAL/AUTO_INCREMENT columns in the INSERT statements.
'''
        # query LLM to generate dataset
        messages = llm.Message()
        messages.add_message_user(prompt_text)
        
        for attempt in range(max_attempts):
            messages.print_chat()
            try:
                answer = llm.generate_answer(messages, json_format=llm.models.Schema) 
                assert isinstance(answer, llm.models.Schema), "The response is not in the expected JSON format."

                # parse CREATE TABLEs
                parsed_tables = []
                for create_table in answer.schema_tables:
                    try:
                        parsed = sqlglot.parse_one(create_table, read="postgres")
                        parsed_tables.append(parsed)
                    except Exception as e:
                        raise SQLParsingError(f"Syntax error in CREATE TABLE generated: {e}", create_table)
                create_commands = [f'{cmd.sql(pretty=True, dialect="postgres")};' for cmd in parsed_tables]

                # parse INSERT INTOs
                parsed_inserts = []
                for create_table in answer.insert_commands:
                    try:
                        parsed = sqlglot.parse_one(create_table, read="postgres")
                        parsed_inserts.append(parsed)
                    except Exception as e:
                        raise SQLParsingError(f"Syntax error in INSERT COMMANDS generated: {e}", create_table)
                insert_commands = [f'{cmd.sql(pretty=True, dialect="postgres")};' for cmd in parsed_inserts]

                catalog = build_catalog_from_sql('; '.join(cmd.sql() for cmd in parsed_tables))
                dav_tools.messages.debug(f'Generated Catalog: {catalog}')

                # check if constraints are satisfied
                errors = []
                for constraint in constraints:
                    try:
                        constraint.validate(catalog, parsed_tables, parsed_inserts)
                    except ConstraintValidationError as e:
                        errors.append(str(e))
                        continue

                # no errors, return dataset
                if not errors:
                    dav_tools.messages.success(f"Dataset generated and validated successfully at attempt {attempt + 1}.")

                    result = Dataset(
                        create_commands=create_commands,
                        insert_commands=insert_commands,
                        domain=domain
                    )
                    # fill cache, since we already have the catalog
                    result._catalog_cache = catalog
                    result._catalog_cache_commands_hash = hash(tuple(create_commands))
                    
                    return result
                
                dav_tools.messages.error(f'Validation failed for attempt {attempt + 1}. Missing requirements: {", ".join(errors)}')
                
                # TODO: use constraint validation errors to give better feedback
                feedback = (
                    f"The previous JSON output was REJECTED because the SQL violated these constraints: {', '.join(errors)}. "
                    "Regenerate the JSON correcting the SQL to satisfy ALL mandatory constraints."
                )
                messages.add_message_user(feedback)

            except SQLParsingError as e:
                dav_tools.messages.error(f"Error during generation (Attempt {attempt + 1}): {e}")
                messages.add_message_user(f"SQL code is not syntactically valid: {str(e)}. Please regenerate valid SQL.")
        
        raise Exception(f'Failed to generate a valid dataset after {max_attempts} attempts.')