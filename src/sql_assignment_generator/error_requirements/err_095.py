from .base import SqlErrorRequirements
from ..constraints import schema as schema_constraints, query as query_constraints
from ..difficulty_level import DifficultyLevel

class Err095_GroupByWithSingletonGroups(SqlErrorRequirements):
    def exercise_constraints(self, difficulty: DifficultyLevel) -> list[query_constraints.QueryConstraint]:
        constraints = super().exercise_constraints(difficulty)

        if difficulty == DifficultyLevel.EASY:
            return [
                *constraints,
                query_constraints.clause_where.Condition(2),
                query_constraints.clause_from.TableReferences(1, 2),
                query_constraints.aggregation.NoAggregation(),
                query_constraints.clause_group_by.GroupBy(1),
                query_constraints.rows.Duplicates(),
                query_constraints.clause_having.NoHaving(),
                query_constraints.subquery.NoSubquery()
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.Condition(2),
                query_constraints.aggregation.NoAggregation(),
                query_constraints.clause_group_by.GroupBy(2),
                query_constraints.rows.Duplicates(),
                query_constraints.subquery.NoSubquery()
            ]
        
        # HARD
        return [
            *constraints,
                query_constraints.clause_where.Condition(3),
                query_constraints.aggregation.NoAggregation(),
                query_constraints.clause_group_by.GroupBy(3),
                query_constraints.rows.Duplicates(),
                query_constraints.subquery.Subqueries()
        ]

    def exercise_extra_details(self) -> str:
        return 'The exercise must require grouping on non-unique columns, i.e., columns that can have duplicate values.'

    def dataset_extra_details(self) -> str:
        return 'INSERT INTO statements must be used to populate the tables with data that contains duplicate values for columns which are used in the GROUP BY clause.'