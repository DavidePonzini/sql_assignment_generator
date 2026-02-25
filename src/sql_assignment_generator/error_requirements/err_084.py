from .base import SqlErrorRequirements
from ..constraints import schema as schema_constraints, query as query_constraints
from ..difficulty_level import DifficultyLevel

class Err084_UnncessaryJoin(SqlErrorRequirements):
    def dataset_constraints(self, difficulty: DifficultyLevel) -> list[schema_constraints.SchemaConstraint]:
        if difficulty == DifficultyLevel.EASY:
            return []
        if difficulty == DifficultyLevel.MEDIUM:
            return[]
        # HARD
        return []

    def exercise_constraints(self, difficulty: DifficultyLevel) -> list[query_constraints.QueryConstraint]:
        if difficulty == DifficultyLevel.EASY:
            constraints = super().exercise_constraints(difficulty)
            return [
                *constraints,
                query_constraints.clause_where.Condition(2),
                query_constraints.clause_from.TableReferences(1, 1),########
                query_constraints.clause_having.NoHaving(),
                query_constraints.subquery.NoSubquery(),
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.Condition(3),
                query_constraints.clause_from.TableReferences(1, 1),########
                query_constraints.aggregation.Aggregation(2),
                query_constraints.subquery.NoSubquery(),
            ]
        
        # HARD
        return [
            *constraints,
            query_constraints.clause_where.Condition(4),
            query_constraints.clause_from.TableReferences(1, 1),########
            query_constraints.aggregation.Aggregation(3),
            query_constraints.subquery.NestedSubqueries()
            
        ]

    def exercise_extra_details(self) -> str:
        return 'In the solution query must be selected ONLY FOREIGN KEY column for at least one table in select.'

    def dataset_extra_details(self) -> str:
        return 'In TABLE CREATION must be FOREIGN KEY relationship between tables.'