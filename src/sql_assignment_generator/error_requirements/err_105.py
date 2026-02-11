from .base import SqlErrorRequirements
from ..constraints import schema as schema_constraints, query as query_constraints
from ..difficulty_level import DifficultyLevel

class Err105_OuterJoinCanBeReplacedByInnerJoin(SqlErrorRequirements):
    def dataset_constraints(self, difficulty: DifficultyLevel) -> list[schema_constraints.SchemaConstraint]:
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
                query_constraints.clause_where.Condition(1),
                query_constraints.clause_from.TableReferences(max_=2),
                query_constraints.clause_having.NoHaving(),
                query_constraints.subquery.NoSubquery()
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.Condition(2),
                query_constraints.clause_from.TableReferences(),
                query_constraints.aggregation.Aggregation(),
                query_constraints.subquery.NoSubquery()
            ]
        
        # HARD
        return [
            *constraints,
                query_constraints.clause_where.Condition(3),
                query_constraints.clause_from.TableReferences(2),
                query_constraints.aggregation.Aggregation(),
                query_constraints.subquery.Subqueries()
        ]

    def exercise_extra_details(self) -> str:
        return 'In the text of natural language query use the word left or right'

    def dataset_extra_details(self) -> str:
        return ''