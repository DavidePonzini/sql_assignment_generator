import random
from .base import SqlErrorRequirements
from ..constraints import schema as schema_constraints, query as query_constraints
from ..difficulty_level import DifficultyLevel

class Err041_DistinctInSumOrAvg(SqlErrorRequirements):
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
        return "The natural language request must contain the word 'distinct' " \
        "but the DISTINCT keyword should not be used in the SQL query."

    def dataset_extra_details(self) -> str:
        return 'The table must have non-key numeric attributes'