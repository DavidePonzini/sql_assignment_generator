from .base import SqlErrorRequirements
from ..constraints import schema as schema_constraints, query as query_constraints
from ..difficulty_level import DifficultyLevel

class Err046_NullInInAnyAllSubquery(SqlErrorRequirements):
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
                query_constraints.clause_where.InAnyAll(1),
                query_constraints.subquery.NestedSubqueries(),
                query_constraints.clause_having.NoHaving()
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.InAnyAll(2),
                query_constraints.subquery.NestedSubqueries(),
            ]
        
        # HARD
        return [
            *constraints,
            query_constraints.clause_where.InAnyAll(3),
            query_constraints.subquery.NestedSubqueries(),
            query_constraints.aggregation.Aggregation()
        ]

    def exercise_extra_details(self) -> str:
        return ''

    def dataset_extra_details(self) -> str:
        return ''