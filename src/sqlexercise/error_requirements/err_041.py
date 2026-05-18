import random
from .base import SqlErrorRequirements
from ..constraints import query as query_constraints
from ..difficulty_level import DifficultyLevel
from ..translatable_text import TranslatableText

class Err041_DistinctInSumOrAvg(SqlErrorRequirements):
    def exercise_constraints(self, difficulty: DifficultyLevel) -> list[query_constraints.QueryConstraint]:
        constraints = super().exercise_constraints(difficulty)
        
        if difficulty == DifficultyLevel.EASY:
            return [
                *constraints,
                random.choice([
                    query_constraints.aggregation.Aggregation(1, allowed_functions=["SUM"]),
                    query_constraints.aggregation.Aggregation(1, allowed_functions=["AVG"]),
                ]),
                query_constraints.clause_having.NoHaving(),
                query_constraints.subquery.NoSubquery(),
                query_constraints.rows.Duplicates()
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.Condition(1),
                random.choice([
                    query_constraints.aggregation.Aggregation(2, allowed_functions=["SUM"]),
                    query_constraints.aggregation.Aggregation(2, allowed_functions=["AVG"]),
                ]),
                query_constraints.subquery.NoSubquery(),
                query_constraints.rows.Duplicates()
            ]
        
        # HARD
        return [
            *constraints,
            query_constraints.clause_where.Condition(2),
            query_constraints.subquery.Subqueries(),
            random.choice([
                query_constraints.aggregation.Aggregation(2, allowed_functions=["SUM"]),
                query_constraints.aggregation.Aggregation(2, allowed_functions=["AVG"]),
            ]),
            query_constraints.rows.Duplicates()
        ]

    def exercise_extra_details(self) -> TranslatableText:
        return TranslatableText(
            "The natural language request must contain the word 'distinct' " \
            "but the DISTINCT keyword should not be used in the SQL query.",
            it="La richiesta in linguaggio naturale deve contenere la parola 'distinti' " \
               "ma la parola chiave DISTINCT non deve essere usata nella query SQL."
        )

    def dataset_extra_details(self) -> TranslatableText:
        return TranslatableText(
            'The table must have non-key numeric attributes',
            it='La tabella deve avere attributi numerici non chiave'
        )