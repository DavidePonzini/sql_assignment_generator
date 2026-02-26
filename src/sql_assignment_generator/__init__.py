'''Generate SQL assignments based on specified SQL errors and difficulty levels.'''

from __future__ import annotations

from typing import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import random

from .difficulty_level import DifficultyLevel
from .domains import random_domain
from .assignments import Assignment, Dataset, Exercise
from .constraints import SchemaConstraint, QueryConstraint
from .error_requirements import SqlErrorRequirements, ERROR_REQUIREMENTS_MAP
from .exceptions import ExerciseGenerationError

import dav_tools
from sql_error_taxonomy import SqlErrors


def generate_assignment(
        errors: list[tuple[SqlErrors, DifficultyLevel]],
        sql_dialect: str = 'postgres',
        *,
        language: str = 'en',
        domain: str | None = None,
        dataset_str: str | None = None,
        shuffle_exercises: bool = False,
        naming_func: Callable[[SqlErrors, DifficultyLevel], str] = lambda error, difficulty: f'{error.name} - {difficulty.name}',
        max_dataset_attempts: int = 3,
        max_exercise_attempts: int = 3,
        max_unique_attempts: int = 3,
        max_workers: int | None = None
    ) -> Assignment:
    '''
    Generate SQL assignments based on the given SQL errors and their corresponding difficulty levels.

    - Exercises are returned in the same order as the input `errors`.
    - Logging happens as soon as possible (during generation), and each message uses the exercise title as its id.
    - Deduplication is global across all generated exercises (thread-safe).

    Args:
        errors (list[tuple[SqlErrors, DifficultyLevel]]): A list of (error, difficulty) pairs.
        sql_dialect (str): The SQL dialect to use for generating the dataset and exercises (e.g., 'postgres', 'mysql').
        domain (str | None): The domain for the assignments. If None, a random domain will be selected.
        language (str): The language for the assignment generation (e.g., 'en' for English).
        dataset_str (str | None): Optional SQL string to use as the dataset. If provided, it will be used instead of generating a new dataset.
        shuffle_exercises (bool): Whether to shuffle exercises to prevent ordering bias (shuffles input order).
        naming_func (Callable[[SqlErrors, DifficultyLevel], str]): Generates exercise titles.
        max_dataset_attempts (int): Maximum retries for generating a valid dataset before skipping.
        max_exercise_attempts (int): Maximum retries for generating a valid exercise before skipping.
        max_unique_attempts (int): Maximum retries to avoid duplicate solutions per (error, difficulty).
        max_workers (int | None): Thread pool size. If None, uses ThreadPoolExecutor default.

    Returns:
        Assignment: The generated assignment (stable order).
    '''
    
    # filter only supported errors
    supported_errors: list[tuple[SqlErrors, DifficultyLevel]] = []
    for error, difficulty in errors:
        if error in ERROR_REQUIREMENTS_MAP:
            supported_errors.append((error, difficulty))
        else:
            dav_tools.messages.warning(f'Skipping unsupported error: {error.name}')

    if not supported_errors:
        raise ValueError('No supported errors provided for assignment generation.')

    if shuffle_exercises:
        random.shuffle(errors)
    

    dav_tools.messages.info(f'Starting assignment generation for {len(supported_errors)} exercises (out of {len(errors)} requested)')

    # convert SqlErrors -> SqlErrorRequirements, keeping difficulty levels
    requirements: list[tuple[SqlErrors, SqlErrorRequirements, DifficultyLevel]] = [
        (
            error,
            ERROR_REQUIREMENTS_MAP[error](language=language),
            difficulty
        )
        for error, difficulty in supported_errors
    ]

    if not dataset_str:
        # No dataset string provided, so we need to generate a dataset based on the requirements of the exercises.
        if domain is None:
            domain = random_domain(language=language)

        dataset_requirements: list[SchemaConstraint] = []
        for _, req, difficulty in requirements:
            dataset_requirements.extend(req.dataset_constraints(difficulty))

        dataset_extra_details: list[str] = [
            req.dataset_extra_details().get(language=language)
            for _, req, _ in requirements
        ]
        dataset_extra_details = [detail for detail in dataset_extra_details if detail.strip()]  # filter out empty details
        dataset_extra_details = list(set(dataset_extra_details))  # deduplicate details

        dav_tools.messages.info(f'Generating dataset for domain: {domain}')
        dataset = Dataset.generate(
            domain=domain,
            sql_dialect=sql_dialect,
            constraints=dataset_requirements,
            extra_details=dataset_extra_details,
            language=language,
            max_attempts=max_dataset_attempts,
        )
    else:
        dataset = Dataset.from_sql(
            sql_str=dataset_str,
            sql_dialect=sql_dialect
        )

    generated_solutions_hashes: set[str] = set()
    hashes_lock = threading.Lock()

    # Serialize log output to avoid interleaving (and to keep dav_tools usage thread-safe).
    log_lock = threading.Lock()

    def _worker(
            idx: int,
            error: SqlErrors,
            difficulty: DifficultyLevel,
            constraints: list[QueryConstraint],
            extra_details: str
    ) -> tuple[int, Exercise | None]:
        title = naming_func(error, difficulty)

        dav_tools.messages.info(f'Starting generation for exercise: {title}')

        last_generated_exercise: Exercise | None = None

        for attempt in range(max_unique_attempts):
            try:
                generated_exercise = Exercise.generate(
                    error=error,
                    difficulty=difficulty,
                    constraints=constraints,
                    extra_details=extra_details,
                    sql_dialect=sql_dialect,
                    dataset=dataset,
                    title=title,
                    max_attempts=max_exercise_attempts,
                    language=language
                )
            except ExerciseGenerationError:
                with log_lock:
                    dav_tools.messages.warning(f'{title}: Skipping exercise generation for {error.name} due to validation failures.')
                return (idx, None)

            last_generated_exercise = generated_exercise
            raw_solution = generated_exercise.solutions[0]
            normalized_solution = raw_solution.sql.lower().strip()

            with hashes_lock:
                is_duplicate = normalized_solution in generated_solutions_hashes
                if not is_duplicate:
                    generated_solutions_hashes.add(normalized_solution)

            if is_duplicate:
                with log_lock:
                    dav_tools.messages.warning(f'{title}: Duplicate solution detected for {error.name} (Attempt {attempt + 1}/{max_unique_attempts}). Regenerating...')
                continue

            return (idx, generated_exercise)

        if last_generated_exercise is not None:
            with log_lock:
                dav_tools.messages.error(f'{title}: Could not generate a UNIQUE exercise for {error.name} after {max_unique_attempts} retries. Skipping.')
        return (idx, None)

    # Pre-allocate so we can preserve ordering no matter completion order.
    ordered_results: list[Exercise | None] = [None] * len(supported_errors)

    if max_workers == 1:
        for idx, (error, requirement, difficulty) in enumerate(requirements):
            i, ex = _worker(
                idx=idx,
                error=error,
                difficulty=difficulty,
                constraints=requirement.exercise_constraints(difficulty),
                extra_details=requirement.exercise_extra_details().get(language=language)
            )
            ordered_results[i] = ex
    else:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(
                    _worker,
                    idx=idx,
                    error=error,
                    difficulty=difficulty,
                    constraints=requirement.exercise_constraints(difficulty),
                    extra_details=requirement.exercise_extra_details().get(language=language)
                )
                for idx, (error, requirement, difficulty) in enumerate(requirements)
            ]
            for fut in as_completed(futures):
                idx, ex = fut.result()
                ordered_results[idx] = ex

    exercises: list[Exercise] = [ex for ex in ordered_results if ex is not None]

    if len(exercises) < len(supported_errors):
        dav_tools.messages.warning(f'Finished generating exercises with some failures. Generated: {len(exercises)}. Unsupported: {len(errors) - len(supported_errors)}. Failed: {len(supported_errors) - len(exercises)}.')
    else:
        dav_tools.messages.success(f'Successfully generated all {len(exercises)} exercises. Unsupported: {len(errors) - len(supported_errors)}.')

    return Assignment(
        dataset=dataset,
        exercises=exercises
    )
