from .base import SqlErrorRequirements
from ..constraints import query as query_constraints
from ..difficulty_level import DifficultyLevel
from ..translatable_text import TranslatableText

class Err063_ImproperNestingOfExpressions(SqlErrorRequirements):
    def exercise_constraints(self, difficulty: DifficultyLevel) -> list[query_constraints.QueryConstraint]:
        constraints = super().exercise_constraints(difficulty)

        if difficulty == DifficultyLevel.EASY:
            return [
                *constraints,
                query_constraints.clause_where.Condition(3),
                query_constraints.clause_from.TableReferences(1, 2),
                query_constraints.subquery.NoSubquery(),
                query_constraints.clause_having.NoHaving()
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.Condition(3),
                query_constraints.subquery.NoSubquery(),
            ]
        
        # HARD
        return [
            *constraints,
            query_constraints.clause_where.Condition(3),
            query_constraints.subquery.Subqueries(),
            query_constraints.aggregation.Aggregation()
        ]

    def exercise_extra_details(self) -> TranslatableText:
        return TranslatableText(
            "The WHERE clause must require nested logical expressions where parentheses are mandatory to ensure correct operator precedence (e.g., '(condition1 OR condition2) AND condition3'). The logic must be realistic and the parentheses must be essential for the query's correctness, not redundant.",
            it="La clausola WHERE deve richiedere espressioni logiche annidate dove le parentesi sono obbligatorie per garantire la corretta precedenza degli operatori (es. '(condizione1 OR condizione2) AND condizione3'). La logica deve essere realistica e le parentesi devono essere essenziali per la correttezza della query, non ridondanti."
        )
    