from .base import SqlErrorRequirements
from ..constraints import schema as schema_constraints, query as query_constraints
from ..difficulty_level import DifficultyLevel

class Err026_TooManyColumnsInSubquery(SqlErrorRequirements):
    def exercise_constraints(self, difficulty: DifficultyLevel) -> list[query_constraints.QueryConstraint]:
        constraints = super().exercise_constraints(difficulty)

        if difficulty == DifficultyLevel.EASY:
            return [
                *constraints,
                query_constraints.clause_where.Condition(1),
                query_constraints.clause_from.TableReferences(0, 1),
                query_constraints.subquery.Subqueries(),
                query_constraints.subquery.NoNesting(),
                query_constraints.clause_having.NoHaving()
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.Condition(2),
                query_constraints.subquery.Subqueries()
            ]
        
        # HARD
        return [
            *constraints,
            query_constraints.clause_where.Condition(3),
            query_constraints.subquery.Subqueries(),
            query_constraints.aggregation.Aggregation(2)
        ]

    def exercise_extra_details(self) -> str:
        return "The exercise should require comparing each row with " \
        "a value from the same row or subset of rows (e.g. 'WHERE balance <comparison operator> (SELECT balance ... WHERE name = 'John')')"
