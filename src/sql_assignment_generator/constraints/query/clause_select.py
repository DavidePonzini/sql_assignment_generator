from .base import QueryConstraint
from sqlscope import Query
from sqlglot import exp
from ...exceptions import ConstraintValidationError

class SelectedColumns(QueryConstraint):
    '''Requires a specific number of columns in the main SELECT clause.'''

    def __init__(self, min_: int = 1, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_

    def validate(self, query: Query) -> None:
        output = query.main_query.output

        columns = len(output.columns)

        if self.max is None:
            if columns < self.min:
                raise ConstraintValidationError(
                    f'Query must select at least {self.min} columns, but selected {columns} columns.'
                )
            return
        if not (self.min <= columns <= self.max):
            raise ConstraintValidationError(
                f'Query must select between {self.min} and {self.max} columns, but selected {columns} columns.'
            )

    @property
    def description(self) -> str:
        if self.max is None:
            return f'Query must select at least {self.min} columns'
        if self.min == self.max:
            return f'Query must select exactly {self.min} columns'
        return f'Query must select between {self.min} and {self.max} columns'

class NoAlias(QueryConstraint):
    '''
    Requires that no columns in the SELECT clause are renamed (no aliases for columns).
    '''

    def validate(self, query: Query) -> None:
        for expression in query.main_query.ast.expressions:
            if isinstance(expression, exp.Alias):
                raise ConstraintValidationError(
                    "Columns in SELECT must not be renamed (must not use aliases)."
                )

    @property
    def description(self) -> str:
        return "Columns in SELECT must not be renamed (must not use aliases)"

class Alias(QueryConstraint):
    '''
        Requires a number of columns in the SELECT clause to be renamed using an alias (AS).
    '''

    def __init__(self, min_: int = 1, max_: int | None = None) -> None:
        super().__init__()
        self.min = min_
        self.max = max_


    def validate(self, query: Query) -> None:
        main_q = query.main_query
        curr_select = main_q[1] if isinstance(main_q, tuple) else main_q

        alias_count = 0
        if hasattr(curr_select, 'ast') and curr_select.ast:
            for expression in curr_select.ast.expressions:
                if isinstance(expression, exp.Alias):
                    alias_count += 1
        else:
            for col in curr_select.output.columns:
                if col.name != col.real_name:
                    alias_count += 1

        if self.max is None:
            if alias_count < self.min:
                raise ConstraintValidationError(
                    f"At least {self.min} columns in SELECT must be renamed using an alias (AS), but only {alias_count} were found."
                )
            return
        
        if not (self.min <= alias_count <= self.max):
            raise ConstraintValidationError(
                f"Between {self.min} and {self.max} columns in SELECT must be renamed using an alias (AS), but {alias_count} were found."
            )

    @property
    def description(self) -> str:
        if self.max is None:
            return f"At least {self.min} columns in SELECT must be renamed using an alias (AS)"
        if self.min == self.max:
            return f"Exactly {self.min} columns in SELECT must be renamed using an alias (AS)"
        return f"Between {self.min} and {self.max} columns in SELECT must be renamed using an alias (AS)"
