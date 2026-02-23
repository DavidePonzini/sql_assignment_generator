from .base import QueryConstraint
from sqlscope import Query
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
        main_q = query.main_query
        curr_select = main_q[1] if isinstance(main_q, tuple) else main_q

        if curr_select is None or isinstance(curr_select, str): return

        if hasattr(curr_select, 'ast') and hasattr(curr_select.ast, 'expressions'):
            for expr in curr_select.ast.expressions:
                if expr.args.get("alias"):
                    raise ConstraintValidationError(self.description)

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

        if curr_select is None or isinstance(curr_select, str): return

        alias_count = 0
        if hasattr(curr_select, 'ast') and hasattr(curr_select.ast, 'expressions'):
            for expr in curr_select.ast.expressions:
                if expr.args.get("alias"):
                    alias_count += 1

        if (self.max is None) and (alias_count < self.min):
            raise ConstraintValidationError(
                f"At least {self.min} columns in SELECT must be renamed using an alias (AS), "
                f"but only {alias_count} were found."
            )
        elif not (self.max is None) and not (self.min <= alias_count <= self.max):
            raise ConstraintValidationError(
                f"Between {self.min} and {self.max} columns in SELECT must be renamed using an alias (AS), "
                f"but {alias_count} were found."
            )

    @property
    def description(self) -> str:
        if self.max is None:
            return f"At least {self.min} columns in SELECT must be renamed using an alias (AS)"
        if self.min == self.max:
            return f"Exactly {self.min} columns in SELECT must be renamed using an alias (AS)"
        return f"Between {self.min} and {self.max} columns in SELECT must be renamed using an alias (AS)"
