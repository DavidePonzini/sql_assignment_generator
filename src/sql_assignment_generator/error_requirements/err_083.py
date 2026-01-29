from .base import SqlErrorRequirements
from ..constraints import schema as schema_constraints, query as query_constraints
from ..difficulty_level import DifficultyLevel

class Err083_UnnecessaryDistinctInSelectClause(SqlErrorRequirements):
    def dataset_constraints(self, difficulty: DifficultyLevel) -> list[schema_constraints.SchemaConstraint]:
        constraints = super().dataset_constraints(difficulty)
        if difficulty == DifficultyLevel.EASY:
            return []
        if difficulty == DifficultyLevel.MEDIUM:
            return[]
        # HARD
        return []

    def exercise_constraints(self, difficulty: DifficultyLevel) -> list[query_constraints.QueryConstraint]:
        constraints = super().exercise_constraints(difficulty)
        if difficulty == DifficultyLevel.EASY:
            return [
                *constraints,
                query_constraints.clause_where.Condition(2),
                query_constraints.clause_from.TableReferences(0, 1),
                query_constraints.rows.NoDuplicates(),
                query_constraints.subquery.NoSubquery(),
                query_constraints.clause_having.NoHaving(),
                
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                query_constraints.clause_where.Condition(3),
                query_constraints.aggregation.Aggregation(2),
                query_constraints.rows.NoDuplicates(),
                query_constraints.subquery.NoSubquery(), 
            ]
        
        # HARD
        return [
            query_constraints.clause_where.Condition(4),
            query_constraints.aggregation.Aggregation(3),
            query_constraints.subquery.Subqueries(),
            query_constraints.rows.NoDuplicates(),
        ]

    def exercise_extra_details(self) -> str:
        return 'In solution there must be no DISTINCT.'

    def dataset_extra_details(self) -> str:
        return ''