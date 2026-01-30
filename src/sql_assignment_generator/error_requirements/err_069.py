from .base import SqlErrorRequirements
from ..constraints import schema as schema_constraints, query as query_constraints
from ..difficulty_level import DifficultyLevel

class Err069_ExpressionInIncorrectClause(SqlErrorRequirements):
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
                query_constraints.clause_where.Condition(1),
                query_constraints.clause_having.Having(1,1),
                query_constraints.subquery.NoSubquery()
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.Condition(3),
                query_constraints.clause_having.Having(1,3),
                query_constraints.aggregation.Aggregation(),
                query_constraints.subquery.NoSubquery()
            ]
        
        # HARD
        return [
            *constraints,
            query_constraints.clause_where.Condition(4),
            query_constraints.clause_having.Having(2,3),
            query_constraints.aggregation.Aggregation(),
            query_constraints.subquery.Subqueries()
        ]

    def exercise_extra_details(self) -> str:
        return ''

    def dataset_extra_details(self) -> str:
        return ''