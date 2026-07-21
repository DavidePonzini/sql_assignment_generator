'''Test script to generate an SQL assignment based on specified error, difficulty, and domain.'''

import dav_tools
import tqdm
from dotenv import load_dotenv
from sqlerrors import SqlErrors
import logging
from sqlscope import Dialect

from src.sqlexercise import generate_assignment
from src.sqlexercise.difficulty_level import DifficultyLevel
from src.sqlexercise import Assignment, Dataset, Exercise

logging.basicConfig(level=logging.DEBUG, filename='test.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

PROGRESS = tqdm.tqdm()

def on_domain_selection(domain: str) -> None:
    dav_tools.messages.info(f'Selected domain: {domain}')

def on_generation_progress(attempt: int, max_attempts: int, label: str) -> None:
    PROGRESS.total = max_attempts
    PROGRESS.n = attempt
    PROGRESS.set_description(label, refresh=False)
    PROGRESS.refresh()

def on_exercise_generation_failure(error: SqlErrors, difficulty: DifficultyLevel) -> None:
    tqdm.tqdm.write(f'Failed to generate exercise for error {error.value} ({error.name}) at difficulty {difficulty.name}')

def print_dataset(dataset: Dataset):
    dav_tools.messages.message(
        '-' * 50,
        dataset.to_sql('datasetExercise'),
        '-' * 50,
        default_text_options=[dav_tools.messages.TextFormat.Color.CYAN],
        sep='\n',
        additional_text_options=[
            [dav_tools.messages.TextFormat.Style.BOLD],
            [],
            [dav_tools.messages.TextFormat.Style.BOLD]
        ]
    )

def print_exercise(exercise: Exercise):
    dav_tools.messages.message(
        exercise.title,
        default_text_options=[dav_tools.messages.TextFormat.Style.BOLD],
    )

    dav_tools.messages.message(
        exercise.request,
        icon_options=[dav_tools.messages.TextFormat.Color.BLUE, dav_tools.messages.TextFormat.Style.BOLD],
        icon='REQ',
    )
    for solution in exercise.solutions:
        dav_tools.messages.message(
            solution.sql,
            default_text_options=[dav_tools.messages.TextFormat.Color.LIGHTGRAY],
            icon_options=[dav_tools.messages.TextFormat.Color.GREEN, dav_tools.messages.TextFormat.Style.BOLD],
            icon='SOL',
        )

def print_assignment(assignment: Assignment):
    print_dataset(assignment.dataset)

    dav_tools.messages.message()
    for exercise in assignment.exercises:
        print_exercise(exercise)
        dav_tools.messages.message()

if __name__ == '__main__':
    load_dotenv()

    errors = [
        # (SqlErrors.AMBIGUOUS_COLUMN, DifficultyLevel.EASY),
        # (SqlErrors.AMBIGUOUS_COLUMN, DifficultyLevel.MEDIUM),
        (SqlErrors.COMPARISON_WITH_NULL, DifficultyLevel.EASY),
        (SqlErrors.COMPARISON_WITH_NULL, DifficultyLevel.MEDIUM),
        # (SqlErrors.COMPARISON_WITH_NULL, DifficultyLevel.HARD),
    ]

    domain = None
    dataset_sql = None
    max_dataset_attempts = 10
    max_exercise_attempts = 10

    assignment = generate_assignment(
        errors=errors,
        db_host='localhost',
        db_port=5432,
        db_user='postgres',
        db_password='password',
        sql_dialect=Dialect.POSTGRES,
        domain=domain,
        language='en',
        dataset_str=dataset_sql,
        max_dataset_attempts=max_dataset_attempts,
        max_exercise_attempts=max_exercise_attempts,
        on_domain_selection=on_domain_selection,
        on_dataset_generation_progress=lambda n, m: on_generation_progress(n, m, 'Dataset Generation'),
        on_exercise_generation_progress=lambda n, m: on_generation_progress(n, m, 'Exercise Generation'),
        on_exercise_generation_failure=on_exercise_generation_failure,
    )

    print_assignment(assignment)