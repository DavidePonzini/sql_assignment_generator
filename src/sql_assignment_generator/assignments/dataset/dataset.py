from collections.abc import Sequence
from dataclasses import dataclass
import dav_tools
import sqlglot
from sqlglot import exp
from sqlscope import Catalog, build_catalog_from_sql

from . import strings
from ...constraints.schema import SchemaConstraint
from ... import llm
from ...constraints import SchemaConstraint, schema as schema_constraints
from ...exceptions import SQLParsingError, ConstraintValidationError, DatasetGenerationError
from ...translatable_text import TranslatableText


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

        return strings.to_sql_format(schema=schema, create_cmds=create_cmds, insert_cmds=insert_cmds)
    
    @staticmethod
    def from_sql(sql_str: str, sql_dialect: str) -> 'Dataset':
        '''Create a Dataset instance from a raw SQL string containing CREATE TABLE and INSERT INTO commands.'''
    
        try:
            parsed = sqlglot.parse(sql_str, read=sql_dialect)
            create_commands = []
            insert_commands = []

            for statement in parsed:
                if isinstance(statement, exp.Create):
                    if statement.kind is not None and statement.kind.upper() != 'TABLE':
                        continue  # skip non-table creation statements, e.g. CREATE SCHEMA
                    create_commands.append(f'{statement.sql()};')
                elif isinstance(statement, exp.Insert):
                    insert_commands.append(f'{statement.sql()};')

            if not create_commands:
                raise ValueError("No CREATE TABLE commands found in the provided SQL string.")
        except Exception as e:
            raise SQLParsingError(f"Error parsing SQL string: {e}", sql_str)

        return Dataset(
            create_commands=create_commands,
            insert_commands=insert_commands,
            domain="CUSTOM_DATASET"
        )
        
    @staticmethod
    def generate(
        domain: str,
        sql_dialect: str,
        constraints: Sequence[SchemaConstraint],
        extra_details: list[str] = [],
        *,
        language: str,
        max_attempts: int = 5
    ) -> 'Dataset':
        '''Generate a SQL dataset based on the specified parameters.'''

        # merge similar constraints
        constraints = schema_constraints.merge_constraints(constraints)

        prompt_text = strings.prompt_generate(
            domain=domain,
            extra_details=extra_details,
            constraints=constraints,
            language=language
        )

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
                        parsed = sqlglot.parse_one(create_table, read=sql_dialect)
                        parsed_tables.append(parsed)
                    except Exception as e:
                        raise SQLParsingError(
                            TranslatableText(
                                f"Syntax error in CREATE TABLE generated: {e}",
                                it=f"Errore di sintassi nella CREATE TABLE generata: {e}"
                            ).get(language),
                            create_table
                        )
                create_commands = [f'{cmd.sql(pretty=True, dialect=sql_dialect)};' for cmd in parsed_tables]

                # parse INSERT INTOs
                parsed_inserts = []
                for create_table in answer.insert_commands:
                    try:
                        parsed = sqlglot.parse_one(create_table, read=sql_dialect)
                        parsed_inserts.append(parsed)
                    except Exception as e:
                        raise SQLParsingError(
                            TranslatableText(
                                f"Syntax error in INSERT COMMANDS generated: {e}",
                                it=f"Errore di sintassi nei comandi INSERT generati: {e}"
                            ).get(language),
                            create_table
                        )
                insert_commands = [f'{cmd.sql(pretty=True, dialect=sql_dialect)};' for cmd in parsed_inserts]

                catalog = build_catalog_from_sql('; '.join(cmd.sql() for cmd in parsed_tables))

                # check if constraints are satisfied
                errors = []
                for constraint in constraints:
                    try:
                        constraint.validate(catalog, parsed_tables, parsed_inserts)
                    except ConstraintValidationError as e:
                        errors.append(e.get(language=language))
                        continue

                # no errors, return dataset
                if not errors:
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
                
                messages.add_message_user(strings.feedback_constraint_violations(errors, language=language))

            except SQLParsingError as e:
                dav_tools.messages.error(f"Error during generation (Attempt {attempt + 1}): {e}")
                messages.add_message_user(
                    TranslatableText(
                        f"Generated SQL code is not syntactically valid: {str(e)}. Please regenerate valid SQL.",
                        it=f"Il codice SQL generato non è sintatticamente valido: {str(e)}. Per favore, rigenera un SQL valido."
                    ).get(language)
                )
        
        raise DatasetGenerationError(f'Failed to generate a valid dataset after {max_attempts} attempts.')