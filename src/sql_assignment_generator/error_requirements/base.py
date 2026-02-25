from ..difficulty_level import DifficultyLevel
from ..constraints import SchemaConstraint, QueryConstraint, schema as schema_constraints
from abc import ABC
from ..difficulty_level import DifficultyLevel

class SqlErrorRequirements(ABC):
    '''Requirements for generating an assignment likely to trigger a specific error'''
    
    def dataset_constraints(self, difficulty: DifficultyLevel) -> list[SchemaConstraint]:
        '''Constraints the dataset must satisfy to likely trigger the error.'''

        # base constraints common to all errors
        if difficulty == DifficultyLevel.EASY:
            return [
                schema_constraints.tables.MinTables(2),
                schema_constraints.tables.MinColumns(2, tables=1),
                schema_constraints.values.MinRows(3)
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                schema_constraints.tables.MinTables(4),
                schema_constraints.tables.MinColumns(4, tables=2),
                schema_constraints.values.MinRows(4)]
        if difficulty == DifficultyLevel.HARD:
            return [
                schema_constraints.tables.MinTables(6),
                schema_constraints.tables.MinColumns(5, tables=3),
                schema_constraints.values.MinRows(5)
            ]

    def exercise_constraints(self, difficulty: DifficultyLevel) -> list[QueryConstraint]:
        '''Constraints the exercise must satisfy to likely trigger the error.'''
        return []

    def exercise_extra_details(self) -> str:
        '''Additional details or instructions for the exercise.'''
        return ''

    def dataset_extra_details(self) -> str:
        '''Additional details or instructions for the dataset.'''
        return ''