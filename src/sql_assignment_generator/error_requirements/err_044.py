import random
from .base import SqlErrorRequirements
from ..constraints import schema as schema_constraints, query as query_constraints
from ..difficulty_level import DifficultyLevel

class Err044_IncorrectWildcard(SqlErrorRequirements):
    def __init__(self):
        super().__init__()
        self._selected_symbols = []

    def _prepare_symbols(self, difficulty: DifficultyLevel):
        """Metodo di supporto per scegliere i simboli in base alla difficoltà."""
        all_wildcards = ["+", "*", "()", "[]", "{}", "^", "%", "_"]
        
        if difficulty == DifficultyLevel.EASY: n = 1
        elif difficulty == DifficultyLevel.MEDIUM: n = 2
        else:  n = 2
        
        self._selected_symbols = random.sample(all_wildcards, k=n)

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

    def exercise_extra_details(self) -> str:
        symbols_str = " and ".join([f"'{s}'" for s in self._selected_symbols])
        return f'''Creates queries that must include {symbols_str} symbol in LIKE wildcard.'''

    def dataset_extra_details(self) -> str:
        return ''