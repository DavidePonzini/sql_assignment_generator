from dataclasses import dataclass
import dav_tools
from .. import llm
import sqlglot
from sqlglot import exp

from sql_error_categorizer.sql_errors import SqlErrors
from ..sql_errors_details import ERROR_DETAILS_MAP
from ..difficulty_level import DifficultyLevel
from ..constraints.schema import TableAmountConstraint, ColumnAmountConstraint, InsertAmountConstraint

@dataclass
class Dataset:
    create_commands: list[str]
    insert_commands: list[str]
    domain: str

    def to_sql(self, schema: str) -> str:
        '''Generate the SQL commands to create and populate the dataset within the specified schema.'''

        # Normalize schema name
        schema = schema.lower().replace(' ', '_')

        create_cmds = '\n'.join(self.create_commands)
        insert_cmds = '\n'.join(self.insert_commands)

        return f'''BEGIN;

DROP SCHEMA IF EXISTS {schema} CASCADE;
CREATE SCHEMA {schema};
SET search_path TO {schema};

{create_cmds}

{insert_cmds}

COMMIT;'''
    
    @staticmethod
    def generate(domain: str, errors: list[tuple[SqlErrors, DifficultyLevel]]) -> 'Dataset':
        unique_schema_constraints_map = {}
        
        #mandatory costraint
        base_constraints = [
            TableAmountConstraint(5),
            ColumnAmountConstraint(3),
            InsertAmountConstraint(3)
        ]
        for c in base_constraints:
            unique_schema_constraints_map[c.description] = c

        #take other costraint inside error
        for error, difficulty in errors:
            error_details = ERROR_DETAILS_MAP[error]
            all_constraints = error_details.constraints.get(difficulty, [])
            
            for constraint in all_constraints: #controll if costraint are in schema module
                if 'schema' in constraint.__class__.__module__:
                    unique_schema_constraints_map[constraint.description] = constraint

        active_constraints = list(unique_schema_constraints_map.values())
        formatted_constraints = '\n'.join(f'- {c.description}' for c in active_constraints)
        
        prompt_text = f'''
        Generate a SQL dataset using follow domain: "{domain}".
        
        MANDATORY CONSTRAINTS:
        {formatted_constraints}
        
        MANDATORY OUTPUT (JSON):
        {{
            "schema_tables": ["CREATE TABLE t1...", "CREATE TABLE t2..."],
            "insert_commands": ["INSERT INTO t1...", "INSERT INTO t2..."]
        }}

        MORE IMPORTANT the INSERT INTO must have following format (Multi-row insert): 
        INSERT INTO tableName VALUES 
            (val1, val2, ...),
            (val3, val4, ...);
        '''
        
        messages = llm.Message()
        messages.add_message_user(prompt_text)

        # ------------------------------------------------------------------
        # CICLO DI GENERAZIONE E VALIDAZIONE (Retry Loop)
        # ------------------------------------------------------------------
        max_attempts = 3
        
        for attempt in range(max_attempts):
            try:
                json_risposta = llm.generate_answer(messages, json_format=llm.models.Schema) 
                print (json_risposta)
                
                parsed_tables = []
                try:
                    for cmd in json_risposta.schema_tables:
                        parsed_tables.append(sqlglot.parse(cmd)[0]) 
                except Exception as e:
                    raise ValueError(f"Syntax error in CREATE TABLE generated: {e}")

                try:
                    all_inserts_sql = "BEGIN; " + "; ".join(json_risposta.insert_commands) + "; END;"
                    inserts_block = sqlglot.parse_one(all_inserts_sql, read="postgres")
                except Exception as e:
                    raise ValueError(f"Syntax error in INSERT COMMANDS generated: {e}")

                #costraint validation
                missing_requirements = []
                
                for constraint in active_constraints:
                    is_satisfied = constraint.validate(inserts_block, parsed_tables)
                    if not is_satisfied: missing_requirements.append(constraint.description)

                if not missing_requirements:
                    dav_tools.messages.success(f"Dataset generated and validated successfully at attempt {attempt + 1}.")
                    return Dataset(
                        create_commands=json_risposta.schema_tables,
                        insert_commands=json_risposta.insert_commands,
                        domain=domain
                    )
                
                dav_tools.messages.error(f'Validation failed for attempt {attempt + 1}. Missing requirements: {", ".join(missing_requirements)}')
                feedback = (
                    f"The previous JSON output was REJECTED because the SQL violated these constraints: {', '.join(missing_requirements)}. "
                    "Regenerate the JSON correcting the SQL to satisfy ALL mandatory constraints."
                )
                messages.add_message_user(feedback)

            except Exception as e:
                dav_tools.messages.error(f"Error during generation (Attempt {attempt + 1}): {e}")
                messages.add_message_user(f"An error occurred: {str(e)}. Please regenerate valid SQL.")
        raise Exception(f'Failed to generate a valid dataset after {max_attempts} attempts.')