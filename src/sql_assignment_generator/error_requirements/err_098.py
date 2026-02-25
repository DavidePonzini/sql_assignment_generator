from .base import SqlErrorRequirements
from ..constraints import schema as schema_constraints, query as query_constraints
from ..difficulty_level import DifficultyLevel

class Err098_UnionByCanReplacedByOr(SqlErrorRequirements):
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
                query_constraints.set_operations.NoUnion(),
                query_constraints.clause_having.NoHaving(),
                query_constraints.subquery.NoSubquery()
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.Condition(2),
                query_constraints.set_operations.NoUnion(),
                query_constraints.aggregation.Aggregation(),
                query_constraints.subquery.NoSubquery()
            ]
        # HARD
        return [
            *constraints,
            query_constraints.clause_where.Condition(3),
            query_constraints.set_operations.NoUnion(),
            query_constraints.aggregation.Aggregation(),
            query_constraints.subquery.NestedSubqueries()
        ]

    def exercise_extra_details(self) -> str:
        return 'The exercise can be solved with a OR in where condition or with UNION but must be use only the OR'

    def dataset_extra_details(self) -> str:
        return ''