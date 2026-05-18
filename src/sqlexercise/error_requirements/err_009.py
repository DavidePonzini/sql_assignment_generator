from .base import SqlErrorRequirements
from ..constraints import schema as schema_constraints, query as query_constraints
from ..difficulty_level import DifficultyLevel

class Err009_Misspellings(SqlErrorRequirements):
    def dataset_constraints(self, difficulty: DifficultyLevel) -> list[schema_constraints.SchemaConstraint]:
        constraints = super().dataset_constraints(difficulty)

        if difficulty == DifficultyLevel.EASY:
            return [
                *constraints,
                schema_constraints.tables.ComplexColumnName(2)
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return[
                *constraints,
                schema_constraints.tables.ComplexColumnName(4)
            ]

        # HARD
        return [
            *constraints,
            schema_constraints.tables.ComplexColumnName(8)
            ]

    def exercise_constraints(self, difficulty: DifficultyLevel) -> list[query_constraints.QueryConstraint]:
        constraints = super().exercise_constraints(difficulty)

        if difficulty == DifficultyLevel.EASY:
            return [
                *constraints,
                query_constraints.clause_where.Condition(),
                query_constraints.clause_from.TableReferences(0, 1),
                query_constraints.subquery.NoSubquery(),
                query_constraints.clause_having.NoHaving()
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
               *constraints,
                query_constraints.clause_where.Condition(2),
                query_constraints.subquery.NoSubquery(),
                query_constraints.aggregation.Aggregation()
            ]
        
        # HARD
        return [
            *constraints,
            query_constraints.clause_where.Condition(2),
            query_constraints.subquery.Subqueries(),
            query_constraints.aggregation.Aggregation()
        ]