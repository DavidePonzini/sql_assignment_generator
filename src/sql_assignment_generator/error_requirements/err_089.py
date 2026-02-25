from .base import SqlErrorRequirements
from ..constraints import schema as schema_constraints, query as query_constraints
from ..difficulty_level import DifficultyLevel

class Err089_UnnecessarilyComplicatedSelectInExistsSubquery(SqlErrorRequirements):
    def exercise_constraints(self, difficulty: DifficultyLevel) -> list[query_constraints.QueryConstraint]:
        constraints = super().exercise_constraints(difficulty)

        if difficulty == DifficultyLevel.EASY:
            return [
               *constraints,
               query_constraints.clause_where.Exists(),
               query_constraints.subquery.Subqueries(1,1),
               query_constraints.subquery.NoNesting(),
               query_constraints.rows.Duplicates(),
               query_constraints.clause_having.NoHaving() 
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.Exists(1),
                query_constraints.subquery.Subqueries(1,2),
                query_constraints.rows.Duplicates(),
                query_constraints.aggregation.Aggregation()
            ]
        # HARD
        return [
            *constraints,
                query_constraints.clause_where.Exists(2),
                query_constraints.subquery.Subqueries(1,2),
                query_constraints.rows.Duplicates(),
                query_constraints.aggregation.Aggregation(2)
        ]

    def exercise_extra_details(self) -> str:
        return 'The exercise must have EXISTS with only one column in SELECT and must not use DISTINCT.'

    def dataset_extra_details(self) -> str:
        return 'INSERT INTO statements must be used to populate the tables with data that contains duplicate values, so that the DISTINCT keyword is necessary to eliminate duplicates from the query results. The dataset should be designed such that without DISTINCT, the query would return duplicate rows, and with DISTINCT, it would return a unique set of rows.'