import random
from .base import SqlErrorRequirements
from ..constraints import schema as schema_constraints, query as query_constraints
from ..difficulty_level import DifficultyLevel

class Err045_MixingGT0WithIsNotNullOrEmptyStringWithNull(SqlErrorRequirements):
    def dataset_constraints(self, difficulty: DifficultyLevel) -> list[schema_constraints.SchemaConstraint]:
        if difficulty == DifficultyLevel.EASY:
            return []
        if difficulty == DifficultyLevel.MEDIUM:
            return[]
        # HARD
        return []

    def exercise_constraints(self, difficulty: DifficultyLevel) -> list[query_constraints.QueryConstraint]:
        constraints = super().exercise_constraints(difficulty)

        selected_comparison = random.choice([
            query_constraints.clause_where.NullComparison(),
            query_constraints.clause_where.NotNullComparison(),
            query_constraints.clause_where.StringComparison(),
            query_constraints.clause_where.EmptyStringComparison()
        ])

        if difficulty == DifficultyLevel.EASY:
            return [
                *constraints,
                selected_comparison,
                query_constraints.clause_having.NoHaving(),
                query_constraints.subquery.NoSubquery()
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return[
                *constraints,
                selected_comparison,
                query_constraints.aggregation.Aggregation(),
                query_constraints.subquery.NoSubquery()
            ]

        # HARD
        return [
            *constraints,
            selected_comparison,
            query_constraints.aggregation.Aggregation(),
            query_constraints.subquery.Subqueries()
        ]


    def exercise_extra_details(self) -> str:
        return ''

    def dataset_extra_details(self) -> str:
        return 'Table must have some NULL, Non-NULL, empty and NUMERIC attributes'