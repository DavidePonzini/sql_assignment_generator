from .base import SqlErrorRequirements
from ..constraints import schema as schema_constraints, query as query_constraints
from ..difficulty_level import DifficultyLevel

class Err079_MissingDistinctFromFunctionParameter(SqlErrorRequirements):
    def dataset_constraints(self, difficulty: DifficultyLevel) -> list[schema_constraints.SchemaConstraint]:
        if difficulty == DifficultyLevel.EASY:
            return [

            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return[

            ]

        # HARD
        return [

            ]

    def exercise_constraints(self, difficulty: DifficultyLevel) -> list[query_constraints.QueryConstraint]:
        if difficulty == DifficultyLevel.EASY:
            return [
                
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                
            ]
        
        # HARD
        return [
            
        ]

    def exercise_extra_details(self) -> str:
        return ''

    def dataset_extra_details(self) -> str:
        return ''