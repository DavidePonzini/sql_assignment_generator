from .base import SqlErrorRequirements
from ..constraints import schema as schema_constraints, query as query_constraints
from ..difficulty_level import DifficultyLevel

class Err021_ComparisonWithNull(SqlErrorRequirements):
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
                query_constraints.clause_where.NullComparison(1, 1),
                query_constraints.clause_from.TableReferences(0, 1),
                query_constraints.subquery.NoSubquery(),
                query_constraints.clause_having.NoHaving()
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.NullComparison(2, 2),
                query_constraints.aggregation.Aggregation(2),
                query_constraints.subquery.NoSubquery()
            ]
        
        # HARD
        return [
            *constraints,
            query_constraints.clause_where.NullComparison(3, 3),
            query_constraints.subquery.Subqueries(),
            query_constraints.aggregation.Aggregation(2)
        ]

    def exercise_extra_details(self) -> str:
        return ''

    def dataset_extra_details(self) -> str:
        return 'Some non-key column in the dataset must have NULL values.'