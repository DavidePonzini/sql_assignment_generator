from typing import Callable
from .difficulty_level import DifficultyLevel
from .domains import random_domain
from .assignments import Assignment, Dataset, Exercise
import random

from sql_error_categorizer.sql_errors import SqlErrors

def generate_assignment(
        errors: list[tuple[SqlErrors, DifficultyLevel]],
        domain: str | None = None,
        *,
        shuffle_exercises: bool = False,
        naming_func: Callable[[SqlErrors, DifficultyLevel], str] = lambda error, difficulty: f'Exercise on {error.name} ({difficulty.name})'
    ) -> Assignment:
    '''
    Generate SQL assignments based on the given SQL errors and their corresponding difficulty levels.

    Args:
        errors (dict[SqlErrors, DifficultyLevel]): A dictionary mapping SQL errors to their difficulty levels.
        domain (str | None): The domain for the assignments. If None, a random domain will be selected.
        shuffle_exercises (bool): Whether to shuffle exercises to prevent ordering bias.
        naming_func (Callable[[SqlErrors, DifficultyLevel], str]): A function to generate exercise titles based on error and difficulty.

    Returns:
        list[Assignment]: A list of generated SQL assignments.
    '''

    if domain is None:
        domain = random_domain()

    dataset = Dataset.generate(domain, errors)

    # Shuffle exercises to prevent ordering bias, if requested
    if shuffle_exercises:
        random.shuffle(errors)

    exercises = [Exercise.generate(error, difficulty, dataset, title=naming_func(error, difficulty)) for error, difficulty in errors]

    return Assignment(
        dataset=dataset,
        exercises=exercises
    )

# TODO: refactor this function inside Exercise/Dataset classes
# def generate_exercise(error: SqlErrors, difficulty: DifficultyLevel, dataset: Dataset) -> Exercise:
#     if error not in ERROR_DETAILS_MAP:
#         raise NotImplementedError(f'SQL Error not supported: {error.name}')

#     error_details = ERROR_DETAILS_MAP[error]
    
#     dav_tools.messages.info(f'Generazione esercizio per errore: {error.name}')
#     dav_tools.messages.info(f'Constaints: {constraints}')
#     dav_tools.messages.info(f'Domain: {dataset.domain}')

#     constraints_list = ERROR_DETAILS_MAP[error].constraints[difficulty]

#     formatted_constraints = '\n'.join(f'- {item}' for item in constraints_list)


#     # TODO: refactor dataset creation in separate function
#     assignment_text =f'''
# ### GUIDELINES ###
# Generate a SQL exercise on the following domain: {domain}. 
# The exercise should NATURALLY tempts student to write a query that fails due to {error_details.description}. 
# The exercise must have the following characteristics: {error_details.characteristics}.

# ### MANDATORY REQUIREMENTS FOR THE EXERCISE ###
# {formatted_constraints}

# #### JSON REQUIRED OUTPUT FORMAT ####
# {{
#     "schema_tables": ["CREATE TABLE command 1...", "CREATE TABLE command 2..."] can create more tables than needed to solve the exercise,
#     "request": "Extract and return ONLY NATURAL LANGUAGE query following the assigned constraints. NEVER ask to include mistake. Be concise and clear. Do NOT provide hints or explanations.",
#     "solution": "Only a single and SYNTACTICALLY correct (executable) SQL query following the ASSIGNED CONSTRAINTS. The query must be well-formatted and match with request."
# }}
#     '''

#     messages = llm.Message()
#     messages.add_message_user(assignment_text)

#     for attempt in range(3):
#         answer = llm.generate_answer(
#             messages,
#             json_format=llm.models.Assignment
#         )

#         messages.print_chat()

#         assert isinstance(answer, llm.models.Assignment)

#         is_valid, missing_requirements = is_solution_valid(answer.schema_tables, answer.solution, constraints_list)

#         if is_valid:
#             return answer

#         dav_tools.messages.error(f'Validation failed for attempt {attempt + 1} (error: {error.value}). Missing requirements: {", ".join(missing_requirements)}')
        
#         feedback = (
#             f'The previously SQL solution was WRONG because it was MISSING: {", ".join(missing_requirements)}. '
#             f'''Please regenerate the exercise with the same JSON format as the previous request. 
#             The new SQL query must follows ALL the original mandatory requirements: {formatted_constraints}''')
        
#         messages.add_message_user(feedback)

#     raise Exception(f'Failed to generate a valid assignment after {3} attempts.')

