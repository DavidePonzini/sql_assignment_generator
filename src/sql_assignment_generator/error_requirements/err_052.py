from .base import SqlErrorRequirements
from ..constraints import query as query_constraints
from ..difficulty_level import DifficultyLevel
from ..translatable_text import TranslatableText

class Err052_OrInsteadOfAnd(SqlErrorRequirements):
    def exercise_constraints(self, difficulty: DifficultyLevel) -> list[query_constraints.QueryConstraint]:
        constraints = super().exercise_constraints(difficulty)

        if difficulty == DifficultyLevel.EASY:
            return [
                *constraints,
                query_constraints.clause_where.Condition(2),
                query_constraints.clause_from.TableReferences(1, 1),
                query_constraints.subquery.NoSubquery(),
                query_constraints.clause_having.NoHaving()
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.Condition(3),
                query_constraints.subquery.NoSubquery(),
                query_constraints.aggregation.Aggregation(),
            ]
        
        # HARD
        return [
            *constraints,
            query_constraints.clause_where.Condition(4),
            query_constraints.subquery.Subqueries(),
            query_constraints.aggregation.Aggregation()
        ]

    def exercise_extra_details(self) -> TranslatableText:
        return TranslatableText(
            "Solution query must have multiple AND conditions (e.g. p.film='Eragon' AND p.type='Fantasy').",
            it="La query soluzione deve avere più condizioni AND (es. p.film='Eragon' AND p.type='Fantasy')."
        )
