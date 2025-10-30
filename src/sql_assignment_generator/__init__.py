from .sql_errors import SqlErrors
from .assignments import Assignment
from .difficulty_level import DifficultyLevel


def generate_assignment(error: SqlErrors, difficulty: DifficultyLevel) -> Assignment:
    '''
    Generate an SQL assignment based on the given SQL error and difficulty level.

    Args:
        error (SqlErrors): The SQL error to base the assignment on.
        difficulty (DifficultyLevel): The difficulty level of the assignment.

    Returns:
        Assignment: The generated SQL assignment.
    '''

    # TODO: implement
    return Assignment(
        request='Find all users born after 2000-01-01',
        solution="SELECT * FROM users WHERE birth_date > '2000-01-01';",
        schema='CREATE TABLE users (id INT, name VARCHAR(100), birth_date DATE);',
    )