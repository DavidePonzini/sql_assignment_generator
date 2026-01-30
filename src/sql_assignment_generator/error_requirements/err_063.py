from .base import SqlErrorRequirements
from ..constraints import schema as schema_constraints, query as query_constraints
from ..difficulty_level import DifficultyLevel

class Err063_ImproperNestingOfExpressions(SqlErrorRequirements):
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
                query_constraints.subquery.NoSubquery(),#where nested
                query_constraints.clause_having.NoHaving()
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.subquery.NoSubquery(),
            ]
        
        # HARD
        return [
            *constraints,
            query_constraints.subquery.Subqueries(),
            query_constraints.aggregation.Aggregation()
        ]

    def exercise_extra_details(self) -> str:
        return "Solution query must have multiple condition that must require NESTING " \
        "(e.g. (condizione1 OR condizione2) AND condizione3 -> NESTING are the condition inside parentesis " \
        "which are MANDATORY)."

    def dataset_extra_details(self) -> str:
        return ''