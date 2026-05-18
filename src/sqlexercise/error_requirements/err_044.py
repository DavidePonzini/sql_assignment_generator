import random
from .base import SqlErrorRequirements
from ..constraints import query as query_constraints
from ..difficulty_level import DifficultyLevel
from ..translatable_text import TranslatableText

class Err044_IncorrectWildcard(SqlErrorRequirements):
    def __init__(self, language: str):
        super().__init__(language=language)
        self._selected_symbols = ''

    def _prepare_symbols(self, difficulty: DifficultyLevel):
        '''Metodo di supporto per scegliere i simboli in base alla difficoltà.'''
        all_wildcards = ['+', '*', '()', '[]', '{}', '^', '%', '_']
        
        if difficulty == DifficultyLevel.EASY: n = 1
        elif difficulty == DifficultyLevel.MEDIUM: n = 2
        else:  n = 3
        
        self._selected_symbols = ''.join(random.sample(all_wildcards, k=n))

    def exercise_constraints(self, difficulty: DifficultyLevel) -> list[query_constraints.QueryConstraint]:
        constraints = super().exercise_constraints(difficulty)

        if difficulty == DifficultyLevel.EASY:
            return [
                *constraints,
                query_constraints.clause_where.WildcardLength(1),
                query_constraints.clause_where.WildcardCharacters(
                    required_characters = self._selected_symbols, 
                    min_= len(self._selected_symbols)),
                query_constraints.clause_having.NoHaving(),
                query_constraints.subquery.NoSubquery()
            ]
        if difficulty == DifficultyLevel.MEDIUM:
            return [
                *constraints,
                query_constraints.clause_where.WildcardLength(2),
                query_constraints.clause_where.WildcardCharacters(
                    required_characters = self._selected_symbols, 
                    min_= len(self._selected_symbols)),
                query_constraints.aggregation.Aggregation(),
                query_constraints.subquery.NoSubquery()
            ]
        
        # HARD
        return [
            *constraints,
            query_constraints.clause_where.WildcardLength(3),
            query_constraints.clause_where.WildcardCharacters(
                required_characters = self._selected_symbols, 
                min_= len(self._selected_symbols)),
            query_constraints.aggregation.Aggregation(),
            query_constraints.subquery.Subqueries()
        ]

    def exercise_extra_details(self) -> TranslatableText:
        return TranslatableText(
            f'Creates queries that must include the following symbols in LIKE wildcard: {" and ".join(self._selected_symbols)}',
            it=f'Crea query che devono includere i seguenti simboli nei wildcard di LIKE: {" e ".join(self._selected_symbols)}'
        )
