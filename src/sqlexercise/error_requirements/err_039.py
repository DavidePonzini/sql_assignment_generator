from .base import SqlErrorRequirements
from ..constraints import query as query_constraints
from ..difficulty_level import DifficultyLevel
from ..translatable_text import TranslatableText

class Err039_AndInsteadOfOr(SqlErrorRequirements):
    def exercise_constraints(self, difficulty: DifficultyLevel) -> list[query_constraints.QueryConstraint]:
        constraints = super().exercise_constraints(difficulty)
        
        if difficulty == DifficultyLevel.EASY:
            return [
                *constraints,
                query_constraints.clause_where.MultipleConditionsOnSameColumn(1),
                query_constraints.clause_from.TableReferences(0, 2),
                query_constraints.subquery.NoSubquery(),
                query_constraints.clause_having.NoHaving()
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.MultipleConditionsOnSameColumn(2),
                query_constraints.aggregation.Aggregation(2),
                query_constraints.subquery.NoSubquery()
            ]
        
        # HARD
        return [
            *constraints,
            query_constraints.clause_where.MultipleConditionsOnSameColumn(3),
            query_constraints.aggregation.Aggregation(2),
            query_constraints.subquery.Subqueries()
        ]

    def exercise_extra_details(self) -> TranslatableText:
        return TranslatableText(
            "The exercise must require multiple OR conditions on the same column " \
            "(e.g. p.bornCity='Rome' OR p.bornCity='Genoa'. This represent one column with multiple conditions). " \
            "It is mandatory use the parentesis to give precedence to a separate condition. ",
            it="L'esercizio deve richiedere condizioni OR multiple sulla stessa colonna " \
               "(es. p.cittàNascita='Roma' OR p.cittàNascita='Genova'. Questo rappresenta una colonna con più condizioni). " \
               "E' obbligatorio usare le parentesi per dare precedenza a una condizione separata."
        )