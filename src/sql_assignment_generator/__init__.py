'''Generate SQL assignments based on specified SQL errors and difficulty levels.'''

from __future__ import annotations

from typing import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import random

from .difficulty_level import DifficultyLevel
from .domains import random_domain
from .assignments import Assignment, Dataset, Exercise

import dav_tools
from sql_error_taxonomy import SqlErrors


def generate_assignment(
        errors: list[tuple[SqlErrors, DifficultyLevel]],
        domain: str | None = None,
        *,
        shuffle_exercises: bool = False,
        naming_func: Callable[[SqlErrors, DifficultyLevel], str] = lambda error, difficulty: f'{error.name} - {difficulty.name}',
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
        domain (str | None): The domain for the assignments. If None, a random domain will be selected.
        shuffle_exercises (bool): Whether to shuffle exercises to prevent ordering bias (shuffles input order).
        naming_func (Callable[[SqlErrors, DifficultyLevel], str]): Generates exercise titles.
        max_unique_attempts (int): Maximum retries to avoid duplicate solutions per (error, difficulty).
        max_workers (int | None): Thread pool size. If None, uses ThreadPoolExecutor default.

    Returns:
        Assignment: The generated assignment (stable order).
    '''

    if domain is None:
        domain = random_domain()

    if shuffle_exercises:
        random.shuffle(errors)


    dav_tools.messages.info(f'Generating dataset for domain: {domain}')
    dataset = Dataset.generate(domain, errors)

    generated_solutions_hashes: set[str] = set()
    hashes_lock = threading.Lock()

    # Serialize log output to avoid interleaving (and to keep dav_tools usage thread-safe).
    log_lock = threading.Lock()

    def _normalize_solution(solution: str) -> str:
        return ' '.join(solution.split()).lower()

    def _log(level: str, msg: str, *, message_id: str) -> None:
        # "each message also has the exercises name as its id"
        with log_lock:
            try:
                if level == 'warning':
                    dav_tools.messages.warning(f'{message_id}: {msg}')
                else:
                    dav_tools.messages.error(f'{message_id}: {msg}')
            except TypeError:
                # If dav_tools.messages.<level> doesn't support id=..., fall back gracefully.
                prefix = f'[{message_id}] '
                if level == 'warning':
                    dav_tools.messages.warning(prefix + msg)
                else:
                    dav_tools.messages.error(prefix + msg)

    def _worker(idx: int, error: SqlErrors, difficulty: DifficultyLevel) -> tuple[int, Exercise | None]:
        title = naming_func(error, difficulty)

        dav_tools.messages.info(f'Starting generation for exercise: {title}')

        last_generated_exercise: Exercise | None = None

        for attempt in range(max_unique_attempts):
            generated_exercise = Exercise.generate(error, difficulty, dataset, title=title)
            last_generated_exercise = generated_exercise

            if generated_exercise is None:
                _log(
                    'warning',
                    f'Skipping exercise generation for {error.name} due to validation failures.',
                    message_id=title
                )
                return (idx, None)

            raw_solution = generated_exercise.solutions[0]
            normalized_solution = _normalize_solution(raw_solution)

            with hashes_lock:
                is_duplicate = normalized_solution in generated_solutions_hashes
                if not is_duplicate:
                    generated_solutions_hashes.add(normalized_solution)

            if is_duplicate:
                _log(
                    'warning',
                    f'Duplicate solution detected for {error.name} (Attempt {attempt + 1}/{max_unique_attempts}). Regenerating...',
                    message_id=title
                )
                continue

            return (idx, generated_exercise)

        if last_generated_exercise is not None:
            _log(
                'error',
                f'Could not generate a UNIQUE exercise for {error.name} after {max_unique_attempts} retries. Skipping.',
                message_id=title
            )

        return (idx, None)

    # Pre-allocate so we can preserve ordering no matter completion order.
    ordered_results: list[Exercise | None] = [None] * len(errors)

    if max_workers == 1:
        for idx, (error, difficulty) in enumerate(errors):
            i, ex = _worker(idx, error, difficulty)
            ordered_results[i] = ex
    else:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(_worker, idx, error, difficulty)
                for idx, (error, difficulty) in enumerate(errors)
            ]
            for fut in as_completed(futures):
                idx, ex = fut.result()
                ordered_results[idx] = ex

    exercises: list[Exercise] = [ex for ex in ordered_results if ex is not None]

    return Assignment(
        dataset=dataset,
        exercises=exercises
    )
