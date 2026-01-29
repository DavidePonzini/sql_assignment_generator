from .base import SqlErrorRequirements
from ..constraints import schema as schema_constraints, query as query_constraints
from ..difficulty_level import DifficultyLevel

class Err012_FailureToSpecifyColumnNameTwice(SqlErrorRequirements):
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
                query_constraints.clause_where.MultipleConditionsOnSameColumn(),
                query_constraints.subquery.NoSubquery(),
                query_constraints.clause_having.NoHaving()
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.MultipleConditionsOnSameColumn(2),
                query_constraints.subquery.NoSubquery(),
                query_constraints.aggregation.Aggregation()
            ]
        
        # HARD
        return [
            *constraints,
            query_constraints.clause_where.MultipleConditionsOnSameColumn(2),
            query_constraints.subquery.Subqueries(),
            query_constraints.aggregation.Aggregation()
        ]

    def exercise_extra_details(self) -> str:
        return "Solution query must have MULTIPLE CONDITION on the SAME COLUMN (e.g. p.film='Alien' OR p.film='Superman' this represent one column with MULTIPLE CONDITION). " \
            "Solution must not have IN format like 'position IN ('Manager', 'Supervisor')' but I want this format 'position ='Manager' OR position = 'Supervisor''" \
            "exercise should naturally tempts student to make a mistake that can cause 'miss column name' errors (e.g. WHERE city='Boston' OR 'Chicago')."

    def dataset_extra_details(self) -> str:
        return ''