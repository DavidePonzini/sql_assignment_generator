from .base import SqlErrorRequirements
from ..constraints import schema as schema_constraints, query as query_constraints
from ..difficulty_level import DifficultyLevel

class Err089_UnnecessarilyComplicatedSelectInExistsSubquery(SqlErrorRequirements):
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
               query_constraints.clause_where.Exists(),
               query_constraints.subquery.Subqueries(1,1),
               query_constraints.rows.NoDuplicates(),
               query_constraints.clause_having.NoHaving() 
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.Exists(1),
                query_constraints.subquery.Subqueries(1,1),
                query_constraints.rows.NoDuplicates(),
                query_constraints.aggregation.Aggregation()
            ]
        # HARD
        return [
            *constraints,
                query_constraints.clause_where.Exists(2),
                query_constraints.subquery.Subqueries(1,1),
                query_constraints.rows.NoDuplicates(),
                query_constraints.aggregation.Aggregation(2)
        ]

    def exercise_extra_details(self) -> str:
        return 'The exercise must have EXISTS with only one column in SELECT and WITHOUT DISTINCT.'

    def dataset_extra_details(self) -> str:
        return ''