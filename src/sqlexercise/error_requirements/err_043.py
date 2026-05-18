from .base import SqlErrorRequirements
from ..constraints import query as query_constraints
from ..difficulty_level import DifficultyLevel
from ..translatable_text import TranslatableText

class Err043_WildcardsWithoutLike(SqlErrorRequirements):
    def exercise_constraints(self, difficulty: DifficultyLevel) -> list[query_constraints.QueryConstraint]:
        constraints = super().exercise_constraints(difficulty)

        if difficulty == DifficultyLevel.EASY:
            return [
                *constraints,
                query_constraints.clause_where.WildcardLength(1),
                query_constraints.clause_from.TableReferences(0, 1),
                query_constraints.clause_having.NoHaving(),
                query_constraints.subquery.NoSubquery()
                
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.WildcardLength(2),
                query_constraints.aggregation.Aggregation(),
                query_constraints.subquery.NoSubquery()
            ]
        
        # HARD
        return [
            *constraints,
            query_constraints.clause_where.WildcardLength(3),
            query_constraints.aggregation.Aggregation(),
            query_constraints.subquery.Subqueries()
        ]

    def exercise_extra_details(self) -> TranslatableText:
        return TranslatableText(
            'In the exercise there are WILDCARD with whole words longer than 5 characters.',
            it='Nell\'esercizio ci sono WILDCARD con parole intere più lunghe di 5 caratteri.'
        )
