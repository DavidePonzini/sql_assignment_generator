from sql_error_categorizer.sql_errors import SqlErrors
from .assignments import Assignment, random_domain
from .difficulty_level import DifficultyLevel

from .sql_errors_details import ERROR_DETAILS_MAP


def generate_assignment(domain: str, error: SqlErrors, difficulty: DifficultyLevel) -> Assignment:
    '''
    Generate an SQL assignment based on the given SQL error and difficulty level.

    Args:
        error (SqlErrors): The SQL error to base the assignment on.
        difficulty (DifficultyLevel): The difficulty level of the assignment.

    Returns:
        Assignment: The generated SQL assignment.
    '''

    try:
        error_details = ERROR_DETAILS_MAP[error]
    except KeyError:
        raise ValueError(f"SQL Error not found: {error.name}")
    
    if not domain:
        domain = random_domain()

    print(f"Generazione esercizio per errore: {error.name}")
    print(f"Difficulty: {difficulty.name}")
    print(f"Domain: {domain}")

    #return Assignment.generate_from_ai_text(domain, error_details, difficulty)
    assignment_object = Assignment.generate_from_ai_html(domain, error_details, difficulty)
    return str(assignment_object)
