'''Generate SQL assignments based on specified SQL errors and difficulty levels.'''

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
        naming_func: Callable[[SqlErrors, DifficultyLevel], str] = lambda error, difficulty: f'{error.name} - {difficulty.name}'
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