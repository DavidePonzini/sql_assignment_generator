from .base import SqlErrorRequirements
from ..constraints import schema as schema_constraints, query as query_constraints
from ..difficulty_level import DifficultyLevel

class Err042_DistinctThatMightRemoveImportantDuplicates(SqlErrorRequirements):
    def exercise_constraints(self, difficulty: DifficultyLevel) -> list[query_constraints.QueryConstraint]:
        constraints = super().exercise_constraints(difficulty)

        if difficulty == DifficultyLevel.EASY:
            return [
                *constraints,
                query_constraints.clause_where.Condition(1),
                query_constraints.clause_from.TableReferences(1, 2),
                query_constraints.aggregation.NoAggregation(),
                query_constraints.clause_group_by.NoGroupBy(),
                query_constraints.rows.Duplicates(),
                query_constraints.clause_having.NoHaving(),
                query_constraints.subquery.NoSubquery()
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.Condition(2),
                query_constraints.aggregation.NoAggregation(),
                query_constraints.clause_group_by.NoGroupBy(),
                query_constraints.rows.Duplicates(),
                query_constraints.subquery.NoSubquery()
            ]
        
        # HARD
        return [
            *constraints,
            query_constraints.clause_where.Condition(2),
            query_constraints.aggregation.NoAggregation(),
            query_constraints.clause_group_by.NoGroupBy(),
            query_constraints.rows.Duplicates(),
            query_constraints.subquery.Subqueries()
            
        ]

    def exercise_extra_details(self) -> str:
        return "The exercise must require selecting attributes that can cause duplicates such as cities, names, etc." \
        "Attributes that can identify a record (i.e. primary keys or unique attributes) MUST NOT be selected (e.g. phone number, address, etc.)."
