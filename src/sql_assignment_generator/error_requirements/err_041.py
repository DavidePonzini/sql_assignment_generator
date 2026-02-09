import random
from .base import SqlErrorRequirements
from ..constraints import schema as schema_constraints, query as query_constraints
from ..difficulty_level import DifficultyLevel

class Err041_DistinctInSumOrAvg(SqlErrorRequirements):
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
                random.choice([
                    query_constraints.aggregation.Aggregation(1, allowed_functions=["SUM"]),
                    query_constraints.aggregation.Aggregation(1, allowed_functions=["AVG"]),
                ]),
                query_constraints.clause_having.NoHaving(),
                query_constraints.subquery.NoSubquery(),
                query_constraints.clause_group_by.GroupBy(),
                query_constraints.rows.Duplicates()
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.Condition(1),
                random.choice([
                    query_constraints.aggregation.Aggregation(2, allowed_functions=["SUM"]),
                    query_constraints.aggregation.Aggregation(2, allowed_functions=["AVG"]),
                ]),
                query_constraints.subquery.NoSubquery(),
                query_constraints.rows.Duplicates()
            ]
        
        # HARD
        return [
            *constraints,
            query_constraints.clause_where.Condition(2),
            query_constraints.subquery.Subqueries(),
            random.choice([
                query_constraints.aggregation.Aggregation(2, allowed_functions=["SUM"]),
                query_constraints.aggregation.Aggregation(2, allowed_functions=["AVG"]),
            ]),
            query_constraints.rows.Duplicates()
        ]

    def exercise_extra_details(self) -> str:
        return "In the natural language query must have explaination word 'distinct' " \
        "but NOT DISTINCT clausole in query."

    def dataset_extra_details(self) -> str:
        return 'he table must have non-key numeric attributes'