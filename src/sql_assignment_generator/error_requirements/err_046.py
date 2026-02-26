from .base import SqlErrorRequirements
from ..constraints import query as query_constraints
from ..difficulty_level import DifficultyLevel
from ..translatable_text import TranslatableText

class Err046_NullInInAnyAllSubquery(SqlErrorRequirements):
    def exercise_constraints(self, difficulty: DifficultyLevel) -> list[query_constraints.QueryConstraint]:
        constraints = super().exercise_constraints(difficulty)

        if difficulty == DifficultyLevel.EASY:
            return [
                *constraints,
                query_constraints.clause_where.InAnyAll(1),
                query_constraints.subquery.Subqueries(),
                query_constraints.subquery.NoNesting(),
                query_constraints.clause_having.NoHaving()
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.InAnyAll(2),
            ]
        
        # HARD
        return [
            *constraints,
            query_constraints.clause_where.InAnyAll(3),
            query_constraints.aggregation.Aggregation()
        ]

    def exercise_extra_details(self) -> TranslatableText:
        return TranslatableText(
            'The exercise must involve a subquery that returns at least one nullable value.',
            it='L\'esercizio deve coinvolgere una subquery che restituisce almeno un valore NULL.'
        )

    def dataset_extra_details(self) -> TranslatableText:
        return TranslatableText(
            'Dataset must contain NULL values.',
            it='Il dataset deve contenere valori NULL.'
        )