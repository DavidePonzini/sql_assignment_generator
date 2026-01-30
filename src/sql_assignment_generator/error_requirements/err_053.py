from .base import SqlErrorRequirements
from ..constraints import schema as schema_constraints, query as query_constraints
from ..difficulty_level import DifficultyLevel

class Err053_ExtraneousNot(SqlErrorRequirements):
    def dataset_constraints(self, difficulty: DifficultyLevel) -> list[schema_constraints.SchemaConstraint]:
        if difficulty == DifficultyLevel.EASY:
            return []
        if difficulty == DifficultyLevel.MEDIUM:
            return[]
        # HARD
        return []

    def exercise_constraints(self, difficulty: DifficultyLevel) -> list[query_constraints.QueryConstraint]:
        constraints = super().exercise_constraints(difficulty)
        if difficulty == DifficultyLevel.EASY:
            return [
                *constraints,
                query_constraints.clause_where.Condition(2),
                query_constraints.subquery.NoSubquery(),
                query_constraints.clause_having.NoHaving()
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.Condition(2),
                query_constraints.subquery.NoSubquery(),
                query_constraints.clause_having.NoHaving()
            ]
        
        # HARD
        return [
            *constraints,
            query_constraints.clause_where.Condition(3),
            query_constraints.subquery.NoSubquery(),
            query_constraints.clause_having.NoHaving()
        ]

    def exercise_extra_details(self) -> str:
        return 'The exercise must have minimum one where without NOT in constraint"'

    def dataset_extra_details(self) -> str:
        return ''