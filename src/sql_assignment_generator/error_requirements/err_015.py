from .base import SqlErrorRequirements
from ..constraints import schema as schema_constraints, query as query_constraints
from ..difficulty_level import DifficultyLevel

class Err015_AggregateFunctionsCannotBeNested(SqlErrorRequirements):
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
                query_constraints.aggregation.Aggregation(2),
                query_constraints.subquery.NoSubquery(),
                query_constraints.clause_having.NoHaving()
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                query_constraints.clause_where.Condition(),
                query_constraints.aggregation.Aggregation(2),
                query_constraints.subquery.NoSubquery()
            ]
        
        # HARD
        return [
            query_constraints.clause_where.Condition(2),
            query_constraints.subquery.Subqueries(),
            query_constraints.aggregation.Aggregation(2)
        ]

    def exercise_extra_details(self) -> str:
        return "Generate a query in natural language that seems to involve one AGGREGATION " \
        "inside another (e.g. 'the book that has the maximum number of sales' and in database doesn't store the sales count)."

    def dataset_extra_details(self) -> str:
        return ''