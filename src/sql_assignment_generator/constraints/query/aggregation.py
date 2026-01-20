from .base import QueryConstraint
from sqlglot import Expression, exp

class NoAggregation(QueryConstraint):
    '''Requires the absence of aggregation functions in the SQL query.'''

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        aggregations_found = list(query_ast.find_all(exp.AggFunc))
        return len(aggregations_found) == 0
    
    @property
    def description(self) -> str:
        return "Exercise must not require any aggregation operations."

class RequireAggregation(QueryConstraint):
    '''
    Requires the presence of aggregation functions in the SQL query.
    
    Args:
        min (int): Minimum number of aggregation functions required. Default is 1.
        max (int | None): Maximum number of aggregation functions allowed. Default is None (no maximum).
        allowed_functions (list[str]): List of allowed aggregation function names (e.g., 'AVG', 'COUNT', 'SUM', 'MAX', 'MIN').
    '''

    def __init__(self,
                 min_: int = 1,
                 max_: int | None = None,
                 *,
                 allowed_functions: list[str] = ['AVG', 'COUNT', 'SUM', 'MAX', 'MIN']
        ) -> None:
        self.min = min_
        self.max = max_ if max_ is not None and max_ > min_ else None

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

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        aggregations_found = list(query_ast.find_all(tuple(self.allowed_exps)))
        count = len(aggregations_found)

        if self.max is None:
            return self.min <= count
        return self.min <= count <= self.max
    
    @property
    def description(self) -> str:
        functions = ', '.join(self.allowed_functions)

        if self.max is None:
            return f'Exercise must require at least {self.min} aggregation function(s) of type(s): {functions}'
        elif self.min == self.max:
            return f'Exercise must require exactly {self.min} aggregation function(s) of type(s): {functions}'
        else:
            return f'Exercise must require between {self.min} and {self.max} aggregation function(s) of type(s): {functions}'