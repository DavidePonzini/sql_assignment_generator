from .base import SqlErrorRequirements
from ..constraints import query as query_constraints
from ..difficulty_level import DifficultyLevel

class Err057_IncorrectComparisonOperatorOrIncorrectValueCompared(SqlErrorRequirements):
    def exercise_constraints(self, difficulty: DifficultyLevel) -> list[query_constraints.QueryConstraint]:
        constraints = super().exercise_constraints(difficulty)

        if difficulty == DifficultyLevel.EASY:
            return [
                *constraints,
                query_constraints.clause_where.StringComparison(2),
                query_constraints.clause_having.NoHaving(),
                query_constraints.subquery.NoSubquery(),
                query_constraints.clause_from.NoJoin()
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return[
                *constraints,
                query_constraints.clause_where.StringComparison(2),
                query_constraints.aggregation.Aggregation(),
                query_constraints.subquery.NoSubquery(),
            ]

        # HARD
        return [
            *constraints,
            query_constraints.clause_where.StringComparison(3),
            query_constraints.aggregation.Aggregation(),
            query_constraints.subquery.Subqueries(),
        ]
