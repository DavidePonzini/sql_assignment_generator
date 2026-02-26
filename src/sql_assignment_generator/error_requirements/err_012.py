from .base import SqlErrorRequirements
from ..constraints import query as query_constraints
from ..difficulty_level import DifficultyLevel
from ..translatable_text import TranslatableText

class Err012_FailureToSpecifyColumnNameTwice(SqlErrorRequirements):
    def exercise_constraints(self, difficulty: DifficultyLevel) -> list[query_constraints.QueryConstraint]:
        constraints = super().exercise_constraints(difficulty)

        if difficulty == DifficultyLevel.EASY:
            return [
                *constraints,
                query_constraints.clause_where.MultipleConditionsOnSameColumn(),
                query_constraints.clause_from.TableReferences(0, 1),
                query_constraints.subquery.NoSubquery(),
                query_constraints.clause_having.NoHaving()
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.MultipleConditionsOnSameColumn(2),
                query_constraints.subquery.NoSubquery(),
                query_constraints.aggregation.Aggregation()
            ]
        
        # HARD
        return [
            *constraints,
            query_constraints.clause_where.MultipleConditionsOnSameColumn(2),
            query_constraints.subquery.Subqueries(),
            query_constraints.aggregation.Aggregation()
        ]

    def exercise_extra_details(self) -> TranslatableText:
        return TranslatableText(
            "Solution query must have multiple simple conditions on the SAME COLUMN (e.g. p.film='Alien' OR p.film='Superman'. This represents one column with MULTIPLE CONDITION). " \
            "Solution must not have IN formatted like 'position IN ('Manager', 'Supervisor')' but I want this formatted as 'position ='Manager' OR position = 'Supervisor''" \
            "exercise should naturally tempts student to make a mistake that can cause 'miss column name' errors (e.g. WHERE city='Boston' OR 'Chicago').",
            it="La query soluzione deve avere più condizioni semplici sulla STESSA COLONNA (es. p.film='Alien' OR p.film='Superman'. Questo rappresenta una colonna con CONDIZIONI MULTIPLE). " \
               "La soluzione non deve usare IN formattato come 'position IN ('Manager', 'Supervisor')', ma voglio che sia formattato come 'position ='Manager' OR position = 'Supervisor''" \
               "l'esercizio dovrebbe naturalmente tentare lo studente a commettere un errore che può causare errori di tipo 'colonna mancante' (es. WHERE city='Boston' OR 'Chicago')."
        )
