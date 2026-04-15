from collections import OrderedDict
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
from ...db import get_database, QueryExecutionError


def _normalize_inserts(parsed_inserts: list[exp.Insert], sql_dialect: str) -> list[str]:
    '''
    Merge multiple INSERT statements for the same table into a single multi-row INSERT.
    Returns the resulting list of SQL strings.
    '''
    grouped: OrderedDict[str, list[exp.Insert]] = OrderedDict()
    for insert in parsed_inserts:
        table_name = insert.this.this.name.lower()
        grouped.setdefault(table_name, []).append(insert)

    result = []
    for table_name, inserts in grouped.items():
        if len(inserts) == 1:
            result.append(f'{inserts[0].sql(pretty=True, dialect=sql_dialect)};')
        else:
            # Check that all INSERTs have matching column lists before merging
            first = inserts[0]
            first_columns = (
                tuple(col.sql() for col in first.this.expressions)
                if isinstance(first.this, exp.Schema)
                else None
            )
            columns_match = all(
                (
                    isinstance(ins.this, exp.Schema)
                    and tuple(col.sql() for col in ins.this.expressions) == first_columns
                )
                if first_columns is not None
                else not isinstance(ins.this, exp.Schema)
                for ins in inserts
            )

            if not columns_match:
                # Column lists differ — keep separate, let constraint handle it
                for insert in inserts:
                    result.append(f'{insert.sql(pretty=True, dialect=sql_dialect)};')
                continue

            all_rows = []
            for insert in inserts:
                values_node = insert.expression
                if isinstance(values_node, exp.Values):
                    all_rows.extend(values_node.expressions)

            new_values = exp.Values(expressions=all_rows)
            merged = exp.Insert(this=first.this, expression=new_values)
            result.append(f'{merged.sql(pretty=True, dialect=sql_dialect)};')

    return result


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
            insert_asts = []

            for statement in parsed:
                if isinstance(statement, exp.Create):
                    if statement.kind is not None and statement.kind.upper() != 'TABLE':
                        continue  # skip non-table creation statements, e.g. CREATE SCHEMA
                    create_commands.append(f'{statement.sql()};')
                elif isinstance(statement, exp.Insert):
                    insert_asts.append(statement)

            if not create_commands:
                raise ValueError("No CREATE TABLE commands found in the provided SQL string.")
        except Exception as e:
            raise SQLParsingError(f"Error parsing SQL string: {e}", sql_str)

        insert_commands = _normalize_inserts(insert_asts, sql_dialect)

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
        db_host: str,
        db_port: int,
        db_user: str,
        db_password: str,
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
            sql_dialect=sql_dialect,
            language=language,
        )

        # query LLM to generate dataset
        messages = llm.Message()
        messages.add_message_user(prompt_text)
        
        for attempt in range(max_attempts):
            # messages.print_chat()
            
            try:
                dav_tools.messages.progress(f'Generating dataset (Attempt {attempt + 1}/{max_attempts})...')

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
                insert_commands = _normalize_inserts(parsed_inserts, sql_dialect)

                # try executing the generated SQL to ensure it's valid and to build the catalog for constraint validation
                dav_tools.messages.progress('Executing SQL...')
                
                with get_database(db_host, db_port, db_user, db_password, sql_dialect) as db:
                    full_sql = '\n'.join(create_commands + insert_commands)
                    try:
                        db.execute(full_sql)
                    except QueryExecutionError as e:
                        raise SQLParsingError(
                            TranslatableText(
                                f"Error executing generated SQL: {e}",
                                it=f"Errore durante l'esecuzione dell'SQL generato: {e}"
                            ).get(language),
                            full_sql
                        )

                # build catalog for constraint validation
                catalog = build_catalog_from_sql('; '.join(cmd.sql() for cmd in parsed_tables))

                # check if constraints are satisfied
                dav_tools.messages.progress('Checking constraints...')
                
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