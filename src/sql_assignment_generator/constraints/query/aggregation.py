from sqlscope import Query
from .base import QueryConstraint
from sqlglot import exp
from ...exceptions import ConstraintValidationError
from ...translatable_text import TranslatableText


class NoAggregation(QueryConstraint):
    '''Requires the absence of aggregation functions in the SQL query.'''

    def validate(self, query: Query) -> None:
        for select in query.selects:
            query_ast = select.ast
            if query_ast is None:
                raise ConstraintValidationError(
                    TranslatableText(
                        f'Invalid query: unable to parse the SQL query: {select.sql}',
                        it=f'Query non valida: impossibile analizzare la query SQL: {select.sql}'
                    )
                )

            aggregations_found = list(query_ast.find_all(exp.AggFunc))
            if len(aggregations_found) > 0:
                raise ConstraintValidationError(
                    TranslatableText(
                        f'Exercise must not require any aggregation operations. Found aggregations: {[agg.sql() for agg in aggregations_found]}',
                        it=f'L\'esercizio non deve richiedere operazioni di aggregazione. Sono state trovate le seguenti aggregazioni: {[agg.sql() for agg in aggregations_found]}'
                    )
                )
    
    @property
    def description(self) -> TranslatableText:
        return TranslatableText(
            'Exercise must not require any aggregation operations.',
            it='L\'esercizio non deve richiedere operazioni di aggregazione.'
        )

class Aggregation(QueryConstraint):
    '''
    Requires the presence of aggregation functions in the SQL query.
    
    Args:
        min (int): Minimum number of aggregation functions required. Default is 1.
        max (int | None): Maximum number of aggregation functions allowed. Default is None (no maximum).
        allowed_functions (list[str]): List of allowed aggregation function names (e.g., 'AVG', 'COUNT', 'SUM', 'MAX', 'MIN').
    '''

    def __init__(
            self,
            min_: int = 1,
            max_: int | None = None,
            *,
            allowed_functions: list[str] = ['AVG', 'COUNT', 'SUM', 'MAX', 'MIN'],
        ) -> None:
        self.min = min_
        self.max = max_

        # normalize allowed functions to uppercase
        self.allowed_functions = [func.upper() for func in allowed_functions]

        # map allowed function names to sqlglot expression types
        self.allowed_exps: list[type[exp.AggFunc]] = []
        if 'AVG' in self.allowed_functions:
            self.allowed_exps.append(exp.Avg)
        if 'COUNT' in self.allowed_functions:
            self.allowed_exps.append(exp.Count)
        if 'SUM' in self.allowed_functions:
            self.allowed_exps.append(exp.Sum)
        if 'MAX' in self.allowed_functions:
            self.allowed_exps.append(exp.Max)
        if 'MIN' in self.allowed_functions:
            self.allowed_exps.append(exp.Min)

    def validate(self, query: Query) -> None:
        all_aggregations_found = []

        for select in query.selects:
            select = select.strip_subqueries()      # get rid of subqueries to avoid double counting
            query_ast = select.ast
            if query_ast is None:
                raise ConstraintValidationError(
                    TranslatableText(
                        f'Invalid query: unable to parse the SQL query: {select.sql}',
                        it=f'Query non valida: impossibile analizzare la query SQL: {select.sql}'
                    )
                )
            
            aggregations_found = list(query_ast.find_all(tuple(self.allowed_exps))) # type: ignore
            all_aggregations_found.extend(aggregations_found)

        count = len(all_aggregations_found)
        if self.max is None:
            if count < self.min:
                raise ConstraintValidationError(
                    TranslatableText(
                        f'Exercise requires at least {self.min} aggregation function(s), but only {count} found: {[agg.sql() for agg in all_aggregations_found]}.',
                        it=f'L\'esercizio richiede almeno {self.min} funzione(i) di aggregazione, ma ne sono state trovate solo {count}: {[agg.sql() for agg in all_aggregations_found]}'
                    )
                )
        elif not (self.min <= count <= self.max):
            raise ConstraintValidationError(
                TranslatableText(
                    f'Exercise requires between {self.min} and {self.max} aggregation function(s), but {count} found: {[agg.sql() for agg in all_aggregations_found]}.',
                    it=f'L\'esercizio richiede tra {self.min} e {self.max} funzioni di aggregazione, ma ne sono state trovate {count}: {[agg.sql() for agg in all_aggregations_found]}'
                )
            )
    
    @property
    def description(self) -> TranslatableText:
        functions = ', '.join(self.allowed_functions)

        if self.max is None:
            return TranslatableText(
                f'Exercise must require at least {self.min} aggregation function(s) of type(s): {functions}',
                it=f'L\'esercizio deve richiedere almeno {self.min} funzione(i) di aggregazione di tipo: {functions}'
            )
        elif self.min == self.max:
            return TranslatableText(
                f'Exercise must require exactly {self.min} aggregation function(s) of type(s): {functions}',
                it=f'L\'esercizio deve richiedere esattamente {self.min} funzione(i) di aggregazione di tipo: {functions}'
            )
        else:
            return TranslatableText(
                f'Exercise must require between {self.min} and {self.max} aggregation function(s) of type(s): {functions}',
                it=f'L\'esercizio deve richiedere tra {self.min} e {self.max} funzioni di aggregazione di tipo: {functions}'
            )