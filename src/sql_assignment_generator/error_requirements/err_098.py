from .base import SqlErrorRequirements
from ..constraints import query as query_constraints
from ..difficulty_level import DifficultyLevel
from ..translatable_text import TranslatableText

class Err098_UnionByCanReplacedByOr(SqlErrorRequirements):
    def exercise_constraints(self, difficulty: DifficultyLevel) -> list[query_constraints.QueryConstraint]:
        constraints = super().exercise_constraints(difficulty)

        if difficulty == DifficultyLevel.EASY:
            return [
                *constraints,
                query_constraints.clause_where.Condition(2),
                query_constraints.clause_from.TableReferences(1,2),
                query_constraints.set_operations.NoUnion(),
                query_constraints.clause_having.NoHaving(),
                query_constraints.subquery.NoSubquery()
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.Condition(2),
                query_constraints.set_operations.NoUnion(),
                query_constraints.aggregation.Aggregation(),
                query_constraints.subquery.NoSubquery()
            ]
        # HARD
        return [
            *constraints,
            query_constraints.clause_where.Condition(3),
            query_constraints.set_operations.NoUnion(),
            query_constraints.aggregation.Aggregation(),
            query_constraints.subquery.Subqueries()
        ]

    def exercise_extra_details(self) -> TranslatableText:
        return TranslatableText(
            "The exercise must require having in the WHERE clause two different conditions connected by OR on the same column",
            it="L'esercizio deve richiedere di avere nella clausola WHERE due condizioni diverse collegate da OR sulla stessa colonna"
        )
    