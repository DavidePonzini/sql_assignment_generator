'''Generate SQL assignments based on specified SQL errors and difficulty levels.'''

from typing import Callable
from .difficulty_level import DifficultyLevel
from .domains import random_domain
from .assignments import Assignment, Dataset, Exercise
import random
import dav_tools

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
    if shuffle_exercises: random.shuffle(errors)

    #exercises = [Exercise.generate(error, difficulty, dataset, title=naming_func(error, difficulty)) for error, difficulty in errors]
    exercises = []
    generated_solutions_hashes = set() #set to track unique solutions
    for error, difficulty in errors:
        #max number of tempt
        max_unique_attempts = 3
        unique_exercise_found = False
        for attempt in range(max_unique_attempts):
            generated_exercise = Exercise.generate(error, difficulty, dataset, title=naming_func(error, difficulty))
            
            #generation failed
            if generated_exercise is None: break

            raw_solution = generated_exercise.solutions[0]
            normalized_solution = " ".join(raw_solution.split()).lower()

            #duplicate case (only problem is if solution is duplicate we can retry but 3 times max and then skip)
            if normalized_solution in generated_solutions_hashes:
                dav_tools.messages.warning(
                    f"Duplicate solution detected for {error.name} (Attempt {attempt+1}/{max_unique_attempts}). Regenerating..."
                )
                continue
            else:
                generated_solutions_hashes.add(normalized_solution)
                exercises.append(generated_exercise)
                unique_exercise_found = True
                break
        
        # if after max attempts we can't find unique exercise we skip
        if not unique_exercise_found and generated_exercise is not None:
             dav_tools.messages.error(f"Could not generate a UNIQUE exercise for {error.name} after {max_unique_attempts} retries. Skipping.")
        elif generated_exercise is None:
             dav_tools.messages.warning(f"Skipping exercise generation for {error.name} due to validation failures.")

    return Assignment(
        dataset=dataset,
        exercises=exercises
    )