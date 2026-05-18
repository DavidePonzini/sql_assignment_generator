from .base import SqlErrorRequirements
from ..constraints import query as query_constraints
from ..difficulty_level import DifficultyLevel

class Err102_InefficientUnion(SqlErrorRequirements):
    def exercise_constraints(self, difficulty: DifficultyLevel) -> list[query_constraints.QueryConstraint]:
        constraints = super().exercise_constraints(difficulty)

        if difficulty == DifficultyLevel.EASY:
            return [
                *constraints,
                query_constraints.clause_where.Condition(2),
                query_constraints.clause_from.NoJoin(),
                query_constraints.set_operations.UnionOfType(True),
                query_constraints.clause_having.NoHaving(),
                query_constraints.subquery.NoSubquery(),
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.Condition(3),
                query_constraints.set_operations.UnionOfType(True),
                query_constraints.subquery.NoSubquery(),
                query_constraints.aggregation.Aggregation()
            ]
        
        # HARD
        return [
           *constraints,
            query_constraints.clause_where.Condition(4),
            query_constraints.set_operations.UnionOfType(True),
            query_constraints.subquery.Subqueries(),
            query_constraints.aggregation.Aggregation()
        ]
