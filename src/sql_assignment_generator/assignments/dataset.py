from collections.abc import Sequence
from dataclasses import dataclass
import dav_tools

from ..constraints.schema import SchemaConstraint
from .. import llm
import sqlglot
from sql_error_taxonomy import SqlErrors
from sqlscope import Catalog, build_catalog_from_sql
from ..sql_errors_details import ERROR_DETAILS_MAP
from ..difficulty_level import DifficultyLevel
from ..constraints import SchemaConstraint, schema as schema_constraints
from ..exceptions import SQLParsingError


default_constraints: dict[DifficultyLevel, Sequence[SchemaConstraint]] = {
    DifficultyLevel.EASY: [
        schema_constraints.tables.MinTables(2),
        schema_constraints.tables.MinColumns(2, tables=1),
        schema_constraints.values.MinRows(3)
    ],
    DifficultyLevel.MEDIUM: [
        schema_constraints.tables.MinTables(4),
        schema_constraints.tables.MinColumns(4, tables=2),
        schema_constraints.values.MinRows(4)
    ],
    DifficultyLevel.HARD: [
        schema_constraints.tables.MinTables(6),
        schema_constraints.tables.MinColumns(5, tables=3),
        schema_constraints.values.MinRows(5)
    ]
}

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
                 *,
                 extra_details: list[str] = [],
                 max_attempts: int = 3
        ) -> 'Dataset':
        '''Generate a SQL dataset based on the specified parameters.'''

        # TODO: add default constraints based on difficulty level of errors
        # they need to be handled in the calling function

        # merge similar constraints
        constraints = schema_constraints.merge_constraints(constraints)

        formatted_constraints = '\n'.join(f'- {c.description}' for c in constraints)
        
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
    "schema_tables": ["CREATE TABLE t1...", "CREATE TABLE t2..."],
    "insert_commands": ["INSERT INTO t1...", "INSERT INTO t2..."]
}}

INSERT INTO statements must have following format (Multi-row insert): 
INSERT INTO tableName VALUES 
    (val_1, val_2, ...),
    (val_n, val_n+1, ...);
'''
        # query LLM to generate dataset
        messages = llm.Message()
        messages.add_message_user(prompt_text)
        
        for attempt in range(max_attempts):
            try:
                answer = llm.generate_answer(messages, json_format=llm.models.Schema) 
                assert isinstance(answer, llm.models.Schema), "The response is not in the expected JSON format."

                # parse CREATE TABLEs
                parsed_tables = []
                for insert_into in answer.schema_tables:
                    try:
                        parsed = sqlglot.parse_one(insert_into, read="postgres")
                        parsed_tables.append(parsed)
                    except Exception as e:
                        raise SQLParsingError(f"Syntax error in CREATE TABLE generated: {e}", insert_into)
                create_commands = [f'{cmd.sql(pretty=True, dialect="postgres")};' for cmd in parsed_tables]

                # parse INSERT INTOs
                parsed_inserts = []
                for insert_into in answer.insert_commands:
                    try:
                        parsed = sqlglot.parse_one(insert_into, read="postgres")
                        parsed_inserts.append(parsed)
                    except Exception as e:
                        raise SQLParsingError(f"Syntax error in INSERT COMMANDS generated: {e}", insert_into)
                insert_commands = [f'{cmd.sql(pretty=True, dialect="postgres")};' for cmd in parsed_inserts]

                catalog = build_catalog_from_sql('\n'.join(cmd.sql() for cmd in parsed_tables))

                # check if constraints are satisfied
                errors = []
                for constraint in constraints:
                    if not constraint.validate(catalog, parsed_tables, parsed_inserts):
                        errors.append(constraint.description)

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