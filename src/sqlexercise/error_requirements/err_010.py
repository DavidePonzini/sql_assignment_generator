from .base import SqlErrorRequirements
from ..constraints import query as query_constraints
from ..difficulty_level import DifficultyLevel
from ..translatable_text import TranslatableText

class Err010_Synonyms(SqlErrorRequirements):
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
            query_constraints.subquery.Subqueries(),
            query_constraints.aggregation.Aggregation()
        ]

    def dataset_extra_details(self) -> TranslatableText:
        return TranslatableText(
            'The identifier column name must NOT be <entity>_id; pick a plausible synonym instead (e.g., <entity>_code, <entity>_key, <entity>_ref, <entity>_number,  etc). ' \
            'Additionally, I want naming conventions NOT to be consistent across tables; different tables must have different naming conventions for similar concepts: e.g. if Table1 uses (first_name, last_name), Table2 uses (name, surname)',
            it='Il nome della colonna identificatore non deve essere <entità>_id; scegliere un sinonimo plausibile invece (es. <entità>_codice, <entità>_chiave, <entità>_rif, <entità>_numero,  ecc). ' \
               'Inoltre, voglio che le convenzioni di denominazione NON siano coerenti tra tabelle; diverse tabelle devono avere convenzioni di denominazione diverse per concetti simili: es. se Tabella1 usa (first_name, last_name), Tabella2 usa (name, surname)'
        )