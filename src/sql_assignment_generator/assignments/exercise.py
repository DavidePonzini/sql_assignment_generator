from dataclasses import dataclass
from sql_error_categorizer.sql_errors import SqlErrors
from ..sql_errors_details import ERROR_DETAILS_MAP
from ..difficulty_level import DifficultyLevel
from .dataset import Dataset


@dataclass
class Exercise:
    title: str
    request: str
    solutions: list[str]

    @staticmethod
    def generate(error: SqlErrors, difficulty: DifficultyLevel, dataset: Dataset, title: str) -> 'Exercise':
        if error not in ERROR_DETAILS_MAP:
            raise NotImplementedError(f'SQL Error not supported: {error.name}')

        # TODO: implement exercise generation logic
        return Exercise(
            title=title,
            request='Do this and that',
            solutions=['SELECT * FROM table;'],
        )