'''Test script to generate an SQL assignment based on specified error, difficulty, and domain.'''

from src.sqlexercise.difficulty_level import DifficultyLevel
from src.sqlexercise import generate_assignment
from src.sqlexercise.exceptions import DatasetGenerationError, ExerciseGenerationError
from src.sqlexercise.error_requirements import ERROR_REQUIREMENTS_MAP

from sql_error_taxonomy import SqlErrors
from dotenv import load_dotenv
from concurrent.futures import ProcessPoolExecutor
import random
import dav_tools

# change these values as needed
DOMAIN = None
DATASET_SQL = None


if __name__ == '__main__':
    load_dotenv()

    # with open('dataset_adbis.sql', 'r') as f:
        # dataset_sql = f.read()

    errors = [
        (SqlErrors.MISSING_COLUMN_FROM_SELECT, DifficultyLevel.HARD),
    ]

    assignment = generate_assignment(
            errors=errors,
            db_host='localhost',
            db_port=5432,
            db_user='postgres',
            db_password='password',
            sql_dialect='postgres',
            domain=DOMAIN,
            language='en',
            dataset_str=DATASET_SQL,
            max_dataset_attempts=10,
            max_exercise_attempts=10,
        )

    dav_tools.messages.message(
        '-' * 50,
        assignment.dataset.to_sql('datasetExercise'),
        '-' * 50,
        default_text_options=[dav_tools.messages.TextFormat.Color.CYAN],
        sep='\n',
        additional_text_options=[
            [dav_tools.messages.TextFormat.Style.BOLD],
            [],
            [dav_tools.messages.TextFormat.Style.BOLD]
        ]
    )

    dav_tools.messages.message()
    
    for exercise in assignment.exercises:
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

        dav_tools.messages.message()
