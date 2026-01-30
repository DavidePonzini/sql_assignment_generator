from .base import SqlErrorRequirements
from ..constraints import schema as schema_constraints, query as query_constraints
from ..difficulty_level import DifficultyLevel

class Err040_ImpliedTautologicalOrInconsistentExpressions(SqlErrorRequirements):
    def dataset_constraints(self, difficulty: DifficultyLevel) -> list[schema_constraints.SchemaConstraint]:
        constraints = super().schema_constraints(difficulty)
        if difficulty == DifficultyLevel.EASY:
            return [
                schema_constraints.MinChecks(1)
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return[
                schema_constraints.MinChecks(2)
            ]
        
        # HARD
        return [
            schema_constraints.MinChecks(3)
        ]

    def exercise_constraints(self, difficulty: DifficultyLevel) -> list[query_constraints.QueryConstraint]:
        constraints = super().exercise_constraints(difficulty)
        if difficulty == DifficultyLevel.EASY:
            return [
                *constraints,
                query_constraints.clause_where.MultipleConditionsOnSameColumn(1),
                query_constraints.subquery.NoSubquery(),
                query_constraints.clause_having.NoHaving()
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.MultipleConditionsOnSameColumn(1),
                query_constraints.aggregation.Aggregation(2),
                query_constraints.subquery.NoSubquery()
            ]
        
        # HARD
        return [
            *constraints,
            query_constraints.clause_where.MultipleConditionsOnSameColumn(2),
            query_constraints.aggregation.Aggregation(2),
            query_constraints.subquery.Subqueries()
        ]

    def exercise_extra_details(self) -> str:
        return "Solution query must have MULTIPLE CONDITION on the SAME COLUMN " \
         "(e.g. p.age < 18 OR p.age >= 0 this represent one column with MULTIPLE CONDITION)."

    def dataset_extra_details(self) -> str:
        return ''