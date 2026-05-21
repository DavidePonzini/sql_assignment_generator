'''Test script to generate an SQL assignment based on specified error, difficulty, and domain.'''

from src.sqlexercise.difficulty_level import DifficultyLevel
from src.sqlexercise import generate_assignment
from src.sqlexercise.exceptions import DatasetGenerationError, ExerciseGenerationError
from src.sqlexercise.error_requirements import ERROR_REQUIREMENTS_MAP

from sqlerrors import SqlErrors
from dotenv import load_dotenv
from concurrent.futures import ProcessPoolExecutor
import random
import dav_tools
from dav_tools import database

# change these values as needed
DOMAIN = None
DATASET_SQL = None

def log_event(label: str, success: bool, items: int):
    db = database.PostgreSQL(
        host='localhost',
        port=5432,
        database='postgres',
        user='postgres',
        password='password')
    
    db.insert(
        schema='sqlexercise',
        table='generation_log',
        data={
            'label': label,
            'success': success,
            'items': items
        }
    )

def _generate_batch(items: int):
    supported_errors: list[SqlErrors] = list(ERROR_REQUIREMENTS_MAP.keys())
    errors: list[tuple[SqlErrors, DifficultyLevel]] = []

    for e in random.sample(supported_errors, items):
        difficulty = random.choice(list(DifficultyLevel))
        errors.append((e, difficulty))

    try:
        generate_assignment(
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
            on_exercise_generation_failure=lambda e,d: log_event('exercise', False, items),
            on_dataset_generation_success=lambda: log_event('dataset', True, items),
            on_exercise_generation_success=lambda e,d: log_event('exercise', True, items),
        )
    except DatasetGenerationError:
        log_event('dataset', False, items)
    except (ValueError, AttributeError, Exception):
        log_event('unknown', False, items)

if __name__ == '__main__':
    load_dotenv()

    dav_tools.argument_parser.add_argument('-d', '--datasets', type=int, help='Number of datasets to generate', default=100)
    dav_tools.argument_parser.add_argument('-e', '--exercises', type=int, help='Number of exercises per dataset', default=5)
    args = dav_tools.argument_parser.args

    with ProcessPoolExecutor() as executor:
        for _ in range(args.datasets):
            executor.submit(_generate_batch, args.exercises)

