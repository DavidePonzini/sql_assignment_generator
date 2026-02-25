from .base import SqlErrorRequirements
from ..constraints import schema as schema_constraints, query as query_constraints
from ..difficulty_level import DifficultyLevel

class Err084_UnncessaryJoin(SqlErrorRequirements):
    def exercise_constraints(self, difficulty: DifficultyLevel) -> list[query_constraints.QueryConstraint]:
        constraints = super().exercise_constraints(difficulty)

        if difficulty == DifficultyLevel.EASY:
            return [
                *constraints,
                query_constraints.clause_where.Condition(2),
                query_constraints.clause_from.TableReferences(1, 1),
                query_constraints.clause_having.NoHaving(),
                query_constraints.subquery.NoSubquery(),
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.Condition(3),
                query_constraints.clause_from.TableReferences(1, 2),
                query_constraints.aggregation.Aggregation(2),
                query_constraints.subquery.NoSubquery(),
            ]
        
        # HARD
        return [
            *constraints,
            query_constraints.clause_where.Condition(4),
            query_constraints.clause_from.TableReferences(2, 3),
            query_constraints.aggregation.Aggregation(3),
            query_constraints.subquery.Subqueries()
            
        ]

    def exercise_extra_details(self) -> str:
        return 'The exercise should require selecting ONLY FOREIGN KEY column for at least one of the tables in the FROM clause.'

    def dataset_extra_details(self) -> str:
        return 'In the CREATE TABLE statements, there must be FOREIGN KEY relationship between tables.'