from dataclasses import dataclass
import sqlglot
from sql_error_categorizer.sql_errors import SqlErrors
from ..sql_errors_details import ERROR_DETAILS_MAP
from ..difficulty_level import DifficultyLevel
from .dataset import Dataset
from .. import llm
import dav_tools


@dataclass
class Exercise:
    '''A SQL exercise consisting of a title, request, and solutions.'''

    title: str
    '''The title of the exercise.'''

    request: str
    '''The natural language request or question for the exercise.'''

    solutions: list[str]
    '''The list of SQL query solutions for the exercise.'''

    difficulty: DifficultyLevel
    '''The difficulty level of the exercise.'''

    @staticmethod
    def generate(error: SqlErrors, difficulty: DifficultyLevel, dataset: Dataset, title: str) -> 'Exercise':
        '''Generate a SQL exercise based on the specified parameters.'''
        if error not in ERROR_DETAILS_MAP:
            raise NotImplementedError(f'SQL Error not supported: {error.name}')

        error_details = ERROR_DETAILS_MAP[error]
        constraints_list = ERROR_DETAILS_MAP[error].constraints[difficulty]

        #filter only query costraint
        query_constraints = [c for c in constraints_list if 'query' in c.__class__.__module__]
        formatted_constraints = '\n'.join(f'- {item.description}' for item in query_constraints)

        #prepare DB for assignment text
        dataset_context = "\n".join(dataset.create_commands) + "\n\n" + "\n".join(dataset.insert_commands)

        assignment_text =f'''
### CONTEXT (DATABASE SCHEMA AND DATA) ###
{dataset_context}

### GUIDELINES ###
Generate a SQL exercise based on the dataset above.
The exercise should NATURALLY tempts student to write a query that fails due to {error_details.description}. 
The exercise must have the following characteristics: {error_details.characteristics}.

### MANDATORY REQUIREMENTS FOR THE EXERCISE ###
{formatted_constraints}

#### JSON REQUIRED OUTPUT FORMAT ####
{{
    "request": "Extract and return ONLY NATURAL LANGUAGE query following the assigned constraints. NEVER ask to include mistake. Be concise and clear. Do NOT provide hints or explanations.",
    "solution": "Only a single and SYNTACTICALLY correct (executable) SQL query following the ASSIGNED CONSTRAINTS. The query must be well-formatted and match with request."
}}
'''
        messages = llm.Message()
        messages.add_message_user(assignment_text)

        #parse dataset table
        parsed_dataset_tables = []
        try:
            for cmd in dataset.create_commands:
                parsed_dataset_tables.append(sqlglot.parse_one(cmd))
        except Exception as e:
             dav_tools.messages.warning(f"Warning: Could not parse dataset tables for validation: {e}")

        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                answer = llm.generate_answer(
                    messages,
                    json_format=llm.models.Assignment
                )
                assert isinstance(answer, llm.models.Assignment)
                try:
                    solution_ast = sqlglot.parse_one(answer.solution)
                except Exception as e:
                    raise ValueError(f"Generated SQL solution contains syntax errors: {e}")

                #constraint validation
                missing_requirements = []
                
                for constraint in query_constraints:
                    if not constraint.validate(solution_ast, parsed_dataset_tables):
                        missing_requirements.append(constraint.description)

                if not missing_requirements:
                    dav_tools.messages.success(f"Exercise '{title}' generated and validated successfully.")
                    return Exercise(
                        title=title,
                        request=answer.request,
                        solutions=[answer.solution],
                        difficulty=difficulty
                    )

                #validetion fail management
                dav_tools.messages.error(f'Validation failed for attempt {attempt + 1} (error: {error.name}). Missing requirements: {", ".join(missing_requirements)}')
                
                feedback = (
                    f'The previously generated solution was REJECTED because it missed the following requirements: {", ".join(missing_requirements)}. '
                    f'Please regenerate the JSON. The SQL solution MUST satisfy ALL the original constraints:\n{formatted_constraints}'
                )
                messages.add_message_user(feedback)
            
            except Exception as e:
                dav_tools.messages.error(f"Error during exercise generation (Attempt {attempt + 1}): {e}")
                messages.add_message_user(f"An error occurred: {str(e)}. Please regenerate valid JSON/SQL.")

        raise Exception(f'Failed to generate a valid exercise for {error.name} after {max_attempts} attempts.')