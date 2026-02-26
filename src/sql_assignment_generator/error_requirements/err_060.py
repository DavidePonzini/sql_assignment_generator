from .base import SqlErrorRequirements
from ..constraints import query as query_constraints
from ..difficulty_level import DifficultyLevel
from ..translatable_text import TranslatableText

class Err060_JoinOnIncorrectColumn(SqlErrorRequirements):
    def exercise_constraints(self, difficulty: DifficultyLevel) -> list[query_constraints.QueryConstraint]:
        constraints = super().exercise_constraints(difficulty)

        if difficulty == DifficultyLevel.EASY:
            return [
                *constraints,
                query_constraints.clause_where.Condition(2),
                query_constraints.clause_having.NoHaving(),
                query_constraints.subquery.NoSubquery(),
                query_constraints.clause_from.TableReferences(1,2)
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.Condition(2),
                query_constraints.aggregation.Aggregation(),
                query_constraints.subquery.NoSubquery(),
                query_constraints.clause_from.TableReferences(1,2)
            ]
        
        # HARD
        return [
            *constraints,
            query_constraints.clause_where.Condition(3),
            query_constraints.aggregation.Aggregation(),
            query_constraints.subquery.Subqueries(),
            query_constraints.clause_from.TableReferences(3)
        ]

    def exercise_extra_details(self) -> TranslatableText:
        return TranslatableText(
            "Solution MUST USE composite FOREIGN KEY in join (e.g. column1 a JOIN column2 b ON (a.col1= b.col1) AND (a.col2 = b.col2))",
            it="La soluzione DEVE USARE una chiave esterna composta in un join (es. column1 a JOIN column2 b ON (a.col1= b.col1) AND (a.col2 = b.col2))"
        )

    def dataset_extra_details(self) -> TranslatableText:
        return TranslatableText(
            'Composite foreign keys must be used in CREATE TABLE statements',
            it='Le chiavi esterne composte devono essere usate nelle istruzioni CREATE TABLE'
        )