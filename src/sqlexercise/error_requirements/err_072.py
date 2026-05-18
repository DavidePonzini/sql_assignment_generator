from .base import SqlErrorRequirements
from ..constraints import query as query_constraints
from ..difficulty_level import DifficultyLevel
from ..translatable_text import TranslatableText

class Err072_MissingDistinctFromSelect(SqlErrorRequirements):
    def exercise_constraints(self, difficulty: DifficultyLevel) -> list[query_constraints.QueryConstraint]:
        constraints = super().exercise_constraints(difficulty)

        if difficulty == DifficultyLevel.EASY:
            return [
                *constraints,
                query_constraints.clause_where.Condition(2),
                query_constraints.rows.Distinct(),
                query_constraints.clause_from.TableReferences(1,2),
                query_constraints.clause_having.NoHaving(),
                query_constraints.subquery.NoSubquery()
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.Condition(3),
                query_constraints.rows.Distinct(),
                query_constraints.aggregation.Aggregation(),
                query_constraints.subquery.NoSubquery()
            ]
        
        # HARD
        return [
            *constraints,
            query_constraints.clause_where.Condition(4),
            query_constraints.rows.Distinct(),
            query_constraints.aggregation.Aggregation(),
            query_constraints.subquery.Subqueries()
        ]

    def exercise_extra_details(self) -> TranslatableText:
        return TranslatableText(
            'The columns in the SELECT clause must be attributes that can contain duplicate values.',
            it='Le colonne nella clausola SELECT devono essere attributi che possono contenere valori duplicati.'
        )

    def dataset_extra_details(self) -> TranslatableText:
        return TranslatableText(
            'INSERT INTO statements must be used to populate the tables with data that contains duplicate values, so that the DISTINCT keyword is necessary to eliminate duplicates from the query results. The dataset should be designed such that without DISTINCT, the query would return duplicate rows, and with DISTINCT, it would return a unique set of rows.',
            it='Le istruzioni INSERT INTO devono essere utilizzate per popolare le tabelle con dati che contengono valori duplicati, in modo che la parola chiave DISTINCT sia necessaria per eliminare i duplicati dai risultati della query. Il dataset deve essere progettato in modo tale che senza DISTINCT, la query restituisca righe duplicate, e con DISTINCT restituisca un insieme unico di righe.'
        )