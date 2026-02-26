from .base import SqlErrorRequirements
from ..constraints import query as query_constraints
from ..difficulty_level import DifficultyLevel
from ..translatable_text import TranslatableText

class Err021_ComparisonWithNull(SqlErrorRequirements):
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

    def dataset_extra_details(self) -> TranslatableText:
        return TranslatableText(
            "Some non-key columns in the dataset must have NULL values.",
            it="Alcune colonne non chiave nel dataset devono avere valori NULL."
        )