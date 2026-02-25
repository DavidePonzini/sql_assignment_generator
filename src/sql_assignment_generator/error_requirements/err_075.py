from .base import SqlErrorRequirements
from ..constraints import schema as schema_constraints, query as query_constraints
from ..difficulty_level import DifficultyLevel

class Err075_IncorrectColumnInOrderByClause(SqlErrorRequirements):
    def exercise_constraints(self, difficulty: DifficultyLevel) -> list[query_constraints.QueryConstraint]:
        constraints = super().exercise_constraints(difficulty)

        if difficulty == DifficultyLevel.EASY:
            return [
               *constraints,
               query_constraints.clause_where.Condition(2),
               query_constraints.clause_order_by.OrderBy(1),
               query_constraints.clause_select.SelectedColumns(2),
                query_constraints.clause_from.TableReferences(1,2),
               query_constraints.clause_having.NoHaving(),
               query_constraints.subquery.NoSubquery()
                
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.Condition(3),
                query_constraints.clause_order_by.OrderBy(2),
                query_constraints.clause_select.SelectedColumns(3),
                query_constraints.aggregation.Aggregation(),
                query_constraints.subquery.NoSubquery()
            ]
        
        # HARD
        return [
            *constraints,
            query_constraints.clause_where.Condition(4),
            query_constraints.clause_order_by.OrderBy(3),
            query_constraints.aggregation.Aggregation(),
            query_constraints.subquery.Subqueries(),
            query_constraints.clause_select.SelectedColumns(3)
        ]

    def exercise_extra_details(self) -> str:
        return "The natural language request must INDIRECTLY define the order in " \
        "which the values should appear in the result table, which the student will need to insert into ORDER BY."
