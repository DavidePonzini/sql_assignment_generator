from dataclasses import dataclass
import dav_tools
from .. import llm
import sqlglot
from sql_error_categorizer.sql_errors import SqlErrors
from ..sql_errors_details import ERROR_DETAILS_MAP
from ..difficulty_level import DifficultyLevel
from ..constraints.schema import TableAmountConstraint, ColumnAmountConstraint, InsertAmountConstraint, HasCheckConstraint, HasSamePrimaryKeyConstraint


@dataclass
class Dataset:
    '''A SQL dataset related to a specific domain, including schema creation and data insertion commands.'''

    create_commands: list[str]
    '''SQL commands to create the database schema.'''

    insert_commands: list[str]
    '''SQL commands to insert data into the database.'''

    domain: str
    '''The domain associated with the dataset.'''

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
    def generate(domain: str, errors: list[tuple[SqlErrors, DifficultyLevel]]) -> 'Dataset':
        '''Generate a SQL dataset based on the specified parameters.'''
        unique_schema_constraints_map = {}
        constraint_ranks = {}
        dataset_characteristics = []
        
        difficulty_order = {
            DifficultyLevel.EASY: 1,
            DifficultyLevel.MEDIUM: 2,
            DifficultyLevel.HARD: 3
        }

        # control the maximum difficulty of errors
        max_difficulty = max((difficulty for _, difficulty in errors), key=lambda d: difficulty_order[d])
        max_rank = difficulty_order[max_difficulty]

        if max_difficulty == DifficultyLevel.EASY:
            minNumberOfTables = 2
            minNumberOfColumnsXtables = 1
            minNumberOfColumns = 2
            minNumberOfInserts = 3
        elif max_difficulty == DifficultyLevel.MEDIUM:
            minNumberOfTables = 4
            minNumberOfColumnsXtables = 2
            minNumberOfColumns = 4
            minNumberOfInserts = 4
        else:  # HARD
            minNumberOfTables = 6
            minNumberOfColumnsXtables = 3
            minNumberOfColumns = 5
            minNumberOfInserts = 5

        # mandatory constraints
        base_constraints = [
            TableAmountConstraint(minNumberOfTables),
            ColumnAmountConstraint(minNumberOfColumnsXtables, minNumberOfColumns),
            InsertAmountConstraint(minNumberOfInserts)
        ]
        
        for c in base_constraints:
            c_type = c.__class__.__name__
            unique_schema_constraints_map[c_type] = c
            constraint_ranks[c_type] = max_rank

        # take other schema constraints inside error
        for error, difficulty in errors:
            error_details = ERROR_DETAILS_MAP[error]
            all_constraints = error_details.constraints.get(difficulty, [])
            current_rank = difficulty_order[difficulty]
            
            # check if constraints are in schema module
            for constraint in all_constraints: 
                if 'schema' in constraint.__class__.__module__:
                    c_type = constraint.__class__.__name__
                    
                    # add or update constraint based on rank
                    if c_type not in constraint_ranks or current_rank > constraint_ranks[c_type]:
                        unique_schema_constraints_map[c_type] = constraint
                        constraint_ranks[c_type] = current_rank

            # check characteristics for dataset
            if error_details.dataset_characteristics.strip():
                dataset_characteristics.append(error_details.dataset_characteristics.strip())
        
        # we have all constraints
        active_constraints = list(unique_schema_constraints_map.values())
        formatted_constraints = '\n'.join(f'- {c.description}' for c in active_constraints)
        
        # dataset characteristics str
        if len(dataset_characteristics) > 0:
            dataset_characteristics_str = "The dataset must have the following characteristics:\n"
            for characteristic in dataset_characteristics:
                dataset_characteristics_str += f"- {characteristic}\n"
        else:
            dataset_characteristics_str = ''
        
        prompt_text = f'''
        Generate a SQL dataset about the following domain: "{domain}".
        {dataset_characteristics_str}

        MANDATORY CONSTRAINTS:
        -FOREIGN KEY attributes should have the REFERENCES keyword inline (e.g. Col TYPE REFERENCES table_name(column_name)).
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
        
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                json_risposta = llm.generate_answer(messages, json_format=llm.models.Schema) 
                assert isinstance(json_risposta, llm.models.Schema), "The response is not in the expected JSON format."

                #parsing CREATE TABLE
                parsed_tables = []
                try:
                    for cmd in json_risposta.schema_tables:
                        parsed_tables.append(sqlglot.parse_one(cmd, read="postgres")) #parse convert string into AST expression list
                except Exception as e:
                    raise ValueError(f"Syntax error in CREATE TABLE generated: {e}")

                #parsing INSERT COMMANDS
                parsed_inserts = []
                try:
                    for cmd in json_risposta.insert_commands:
                        parsed_inserts.append(sqlglot.parse_one(cmd, read="postgres")) #parse_one convert string into AST (single object)
                except Exception as e:
                    raise ValueError(f"Syntax error in INSERT COMMANDS generated: {e}")

                #constraint validation
                missing_requirements = []
                
                for constraint in active_constraints:
                    is_satisfied = False

                    if isinstance(constraint, InsertAmountConstraint):
                        is_satisfied = constraint.validate(parsed_inserts, [])
                    elif isinstance(constraint, (TableAmountConstraint, ColumnAmountConstraint, HasCheckConstraint, HasSamePrimaryKeyConstraint)):
                         is_satisfied = constraint.validate(None, parsed_tables)
                    else: is_satisfied = constraint.validate(parsed_inserts, parsed_tables)
                    if not is_satisfied: missing_requirements.append(constraint.description)

                #if all ok the dataset was created
                if not missing_requirements:
                    dav_tools.messages.success(f"Dataset generated and validated successfully at attempt {attempt + 1}.")
                    return Dataset(
                        create_commands=[f'{cmd.sql(pretty=True, dialect="postgres")};' for cmd in parsed_tables],
                        insert_commands=[f'{cmd.sql(pretty=True, dialect="postgres")};' for cmd in parsed_inserts],
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