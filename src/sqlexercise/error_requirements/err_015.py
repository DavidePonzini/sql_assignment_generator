from .base import SqlErrorRequirements
from ..constraints import query as query_constraints
from ..difficulty_level import DifficultyLevel
from ..translatable_text import TranslatableText

class Err015_AggregateFunctionsCannotBeNested(SqlErrorRequirements):
    def exercise_constraints(self, difficulty: DifficultyLevel) -> list[query_constraints.QueryConstraint]:
        constraints = super().exercise_constraints(difficulty)

        if difficulty == DifficultyLevel.EASY:
            return [
                *constraints,
                query_constraints.aggregation.Aggregation(2),
                query_constraints.clause_from.TableReferences(0, 1),
                query_constraints.subquery.NoSubquery(),
                query_constraints.clause_having.NoHaving()
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.Condition(),
                query_constraints.aggregation.Aggregation(2),
                query_constraints.subquery.NoSubquery()
            ]
        
        # HARD
        return [
            *constraints,
            query_constraints.clause_where.Condition(2),
            query_constraints.subquery.Subqueries(),
            query_constraints.aggregation.Aggregation(2)
        ]

    def exercise_extra_details(self) -> TranslatableText:
        return TranslatableText(
            "Generate a query in natural language that seems to involve one AGGREGATION inside another (e.g. 'the book that has the maximum number of sales' -- and the database doesn't store the sales count).",
            it="Genera una query in linguaggio naturale che sembra coinvolgere un AGGREGATO dentro un altro (es. 'il libro che ha il massimo numero di vendite' -- e il database non memorizza il conteggio delle vendite)."
        )