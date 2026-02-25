from .base import SqlErrorRequirements
from ..constraints import schema as schema_constraints, query as query_constraints
from ..difficulty_level import DifficultyLevel

class Err012_FailureToSpecifyColumnNameTwice(SqlErrorRequirements):
    def exercise_constraints(self, difficulty: DifficultyLevel) -> list[query_constraints.QueryConstraint]:
        constraints = super().exercise_constraints(difficulty)

        if difficulty == DifficultyLevel.EASY:
            return [
                *constraints,
                query_constraints.clause_where.MultipleConditionsOnSameColumn(),
                query_constraints.clause_from.TableReferences(0, 1),
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
        return "Solution query must have multiple simple conditions on the SAME COLUMN (e.g. p.film='Alien' OR p.film='Superman'. This represents one column with MULTIPLE CONDITION). " \
            "Solution must not have IN formatted like 'position IN ('Manager', 'Supervisor')' but I want this formatted as 'position ='Manager' OR position = 'Supervisor''" \
            "exercise should naturally tempts student to make a mistake that can cause 'miss column name' errors (e.g. WHERE city='Boston' OR 'Chicago')."
