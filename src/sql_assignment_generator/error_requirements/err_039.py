from .base import SqlErrorRequirements
from ..constraints import schema as schema_constraints, query as query_constraints
from ..difficulty_level import DifficultyLevel

class Err039_AndInsteadOfOr(SqlErrorRequirements):
    def dataset_constraints(self, difficulty: DifficultyLevel) -> list[schema_constraints.SchemaConstraint]:
        if difficulty == DifficultyLevel.EASY:
            return [

            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return[

            ]

        # HARD
        return [

            ]

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

    def exercise_extra_details(self) -> str:
        return "The exercise must have OR MULTIPLE CONDITION on the SAME COLUMN " \
        "(e.g. p.bornCity='Rome' OR p.bornCity='Genoa' this represent one column with MULTIPLE CONDITION). " \
        "It is mandatory use the parentesis to give precedence to separate condition. "

    def dataset_extra_details(self) -> str:
        return ''