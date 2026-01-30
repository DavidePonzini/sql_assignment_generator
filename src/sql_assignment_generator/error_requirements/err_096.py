from .base import SqlErrorRequirements
from ..constraints import schema as schema_constraints, query as query_constraints
from ..difficulty_level import DifficultyLevel

class Err096_GroupByWithOnlyASingleGroup(SqlErrorRequirements):
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
                query_constraints.aggregation.Aggregation(1),
                query_constraints.clause_group_by.NoGroupBy(),
                query_constraints.clause_having.NoHaving(),
                query_constraints.subquery.NoSubquery()
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.Condition(2),
                query_constraints.aggregation.Aggregation(2),
                query_constraints.clause_group_by.NoGroupBy(),
                query_constraints.clause_having.NoHaving(),
                query_constraints.subquery.NoSubquery()
            ]
        # HARD
        return [
            *constraints,
                query_constraints.clause_where.Condition(3),
                query_constraints.aggregation.Aggregation(2),
                query_constraints.clause_group_by.NoGroupBy(),
                query_constraints.clause_having.NoHaving(),
                query_constraints.subquery.NoSubquery()
        ]

    def exercise_extra_details(self) -> str:
        return 'The solution must have in select ONLY aggregate functions.'

    def dataset_extra_details(self) -> str:
        return ''