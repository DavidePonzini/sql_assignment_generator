from .difficulty_level import DifficultyLevel
from .domains import random_domain
from .sql_errors_details import ERROR_DETAILS_MAP
from . import llm
from .assignments import Assignment
#from .query_sintax import is_solution_valid
import sqlglot
from sqlglot import Expression 

import dav_tools
from sql_error_categorizer.sql_errors import SqlErrors

def generate_assignment(error: SqlErrors, difficulty: DifficultyLevel, domain: str | None = None) -> Assignment:
    '''
    Generate an SQL assignment based on the given SQL error and difficulty level.

    Args:
        error (SqlErrors): The SQL error to base the assignment on.
        difficulty (DifficultyLevel): The difficulty level of the assignment.

    Returns:
        Assignment: The generated SQL assignment.
    '''

    if error not in ERROR_DETAILS_MAP:
        raise NotImplementedError(f'SQL Error not supported: {error.name}')

    error_details = ERROR_DETAILS_MAP[error]
    
    if domain is None:
        domain = random_domain()

    dav_tools.messages.info(f'Generazione esercizio per errore: {error.name}')
    dav_tools.messages.info(f'Difficulty: {difficulty.name}')
    dav_tools.messages.info(f'Domain: {domain}')

    constraints_list = error_details.constraints[difficulty]
    formatted_constraints = '\n'.join(f'- {item.description}' for item in constraints_list)

    assignment_text =f'''
### GUIDELINES ###
Generate a SQL exercise on the following domain: {domain}. 
The exercise should NATURALLY tempts student to write a query that fails due to {error_details.description}. 
The exercise must have the following characteristics: {error_details.characteristics}

### MANDATORY REQUIREMENTS FOR THE EXERCISE ###
{formatted_constraints}

#### JSON REQUIRED OUTPUT FORMAT ####
{{
    "schema_tables": ["CREATE TABLE command 1...", "CREATE TABLE command 2..."] can create more tables than needed to solve the exercise,
    "request": "Extract and return ONLY NATURAL LANGUAGE query following the assigned constraints. NEVER ask to include mistake. Be concise and clear. Do NOT provide hints or explanations.",
    "solution": "Only a single and SYNTACTICALLY correct (executable) SQL query following the ASSIGNED CONSTRAINTS. The query must be well-formatted and match with request."
}}
    '''

    messages = llm.Message()
    messages.add_message_user(assignment_text)

    for attempt in range(3):
        answer = llm.generate_answer(
            messages,
            json_format=Assignment
        )

        messages.print_chat()
        assert isinstance(answer, Assignment)

        # is_valid, missing_requirements = is_solution_valid(answer.schema_tables, answer.solution, constraints_list)

        # if is_valid:
        #     return answer

        parsed_tables = []
        try:
            for table_sql in answer.schema_tables:
                parsed = sqlglot.parse(table_sql)[0]
                parsed_tables.append(parsed)
        except Exception as e:
            raise ValueError(f"Syntax error in CREATE TABLE statements: {e}")

        try:
            parsed_query = sqlglot.parse(answer.solution)[0]
        except Exception as e:
            raise ValueError(f"Syntax error in SOLUTION query: {e}")

        #costraint validation
        missing_requirements = []
        for constraint in constraints_list:
            is_satisfied = constraint.validate(parsed_query, parsed_tables)
            if not is_satisfied:
                missing_requirements.append(constraint.description)

        if not missing_requirements:
            dav_tools.messages.success("Assignment validated successfully.")
            return answer

        dav_tools.messages.error(f'Validation failed for attempt {attempt + 1} (error: {error.value}). Missing requirements: {", ".join(missing_requirements)}')
        
        feedback = (
            f'The previously SQL solution was WRONG because it was MISSING: {", ".join(missing_requirements)}. '
            f'''Please regenerate the exercise with the same JSON format as the previous request. 
            The new SQL query must follows ALL the original mandatory requirements: {formatted_constraints}''')
        
        messages.add_message_user(feedback)

    raise Exception(f'Failed to generate a valid assignment after {3} attempts.')

