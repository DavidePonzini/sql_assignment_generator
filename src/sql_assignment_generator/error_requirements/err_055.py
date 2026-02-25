from .base import SqlErrorRequirements
from ..constraints import schema as schema_constraints, query as query_constraints
from ..difficulty_level import DifficultyLevel

class Err055_SubstitutingExistanceNegation(SqlErrorRequirements):
    def exercise_constraints(self, difficulty: DifficultyLevel) -> list[query_constraints.QueryConstraint]:
        constraints = super().exercise_constraints(difficulty)
        
        if difficulty == DifficultyLevel.EASY:
            return [
                *constraints,
                query_constraints.clause_where.NotExist(1),
                query_constraints.subquery.Subqueries(),
                query_constraints.subquery.NoNesting(),
                query_constraints.clause_from.TableReferences(1,2),
                query_constraints.clause_having.NoHaving()
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.NotExist(1),
                query_constraints.subquery.Subqueries(),
                query_constraints.aggregation.Aggregation(),
            ]
        
        # HARD
        return [
            *constraints,
            query_constraints.clause_where.NotExist(2),
            query_constraints.subquery.Subqueries(),
            query_constraints.aggregation.Aggregation(2),
        ]

    def exercise_extra_details(self) -> str:
        return "The exercise must require selecting all Xs that are associated with all Ys (e.g. customers who " \
        "bought all products in category C, customer who bought all products that cost more than 50, etc.)."
