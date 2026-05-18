from dav_tools import database
from sql_error_taxonomy import SqlErrors
from .difficulty_level import DifficultyLevel
import datetime

ERRORS: list[SqlErrors] = []
DIFFICULTIES: list[DifficultyLevel] = []
START_TS: datetime.datetime = datetime.datetime.now()
DOMAIN: str = 'NOT_SET'

def log_message(message: str, details: str | None, *, is_dataset: bool, attempt: int, attempt_max: int, sql: str | None) -> None:
    '''Log a message with a consistent format.'''

    return

    db = database.PostgreSQL('localhost', 5432, 'postgres', 'postgres', 'password')

    with db.connect() as conn:
        conn.insert(
            schema='sqlexercise',
            table='generation_logs',
            data={
                'message': message,
                'details': details,
                'errors': [e.value for e in ERRORS],
                'difficulties': [d.value for d in DIFFICULTIES],
                'is_dataset': is_dataset,
                'attempt': attempt,
                'attempt_max': attempt_max,
                'start_ts': START_TS,
                'sql': sql,
                'domain': DOMAIN,
            }
        )