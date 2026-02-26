from .base import SqlErrorRequirements
from ..constraints import query as query_constraints
from ..difficulty_level import DifficultyLevel
from ..translatable_text import TranslatableText

class Err055_SubstitutingExistanceNegation(SqlErrorRequirements):
    def exercise_constraints(self, difficulty: DifficultyLevel) -> list[query_constraints.QueryConstraint]:
        constraints = super().exercise_constraints(difficulty)
        
        if difficulty == DifficultyLevel.EASY:
            return [
                *constraints,
                query_constraints.clause_where.NotExist(1),
                query_constraints.subquery.Subqueries(),
                query_constraints.subquery.NoNesting(),
                query_constraints.clause_from.TableReferences(1,2),
                query_constraints.clause_having.NoHaving()
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.NotExist(1),
                query_constraints.subquery.Subqueries(),
                query_constraints.aggregation.Aggregation(),
            ]
        
        # HARD
        return [
            *constraints,
            query_constraints.clause_where.NotExist(2),
            query_constraints.subquery.Subqueries(),
            query_constraints.aggregation.Aggregation(2),
        ]

    def exercise_extra_details(self) -> TranslatableText:
        return TranslatableText(
            "The exercise must require selecting all Xs that are associated with all Ys (e.g. customers who bought all products in category C, customer who bought all products that cost more than 50, etc.).",
            it="L'esercizio deve richiedere la selezione di tutti gli X associati a tutti gli Y (es. clienti che hanno comprato tutti i prodotti nella categoria C, cliente che ha comprato tutti i prodotti che costano più di 50, ecc.)."
        )
