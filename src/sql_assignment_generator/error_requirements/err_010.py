from .base import SqlErrorRequirements
from ..constraints import schema as schema_constraints, query as query_constraints
from ..difficulty_level import DifficultyLevel

class Err010_Synonyms(SqlErrorRequirements):
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
                query_constraints.clause_where.Condition(),
                query_constraints.clause_from.TableReferences(0, 1),
                query_constraints.subquery.NoSubquery(),
                query_constraints.clause_having.NoHaving()
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.Condition(2),
                query_constraints.subquery.NoSubquery(),
                query_constraints.aggregation.Aggregation()
            ]
        
        # HARD
        return [
            *constraints,
            query_constraints.clause_where.Condition(3),
            query_constraints.subquery.NestedSubqueries(),
            query_constraints.aggregation.Aggregation()
        ]

    def exercise_extra_details(self) -> str:
        return ''

    def dataset_extra_details(self) -> str:
        return 'The identifier column name must NOT be <entity>_id; pick a plausible synonym instead (e.g., <entity>_code, <entity>_key, <entity>_ref, <entity>_number,  etc). ' \
        'Additionally, I  want  naming conventions NOT to be consistent across tables; different  tables must have different naming conventions for similar concepts: e.g. if Table1 uses (first_name, last_name), Table2 uses (name, surname)'