from .base import QueryConstraint
from sqlglot import Expression, exp

class NoAlias(QueryConstraint):
    '''
    Requires that NO columns in the SELECT clause are renamed (no aliases for columns).
    '''

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        # find the main SELECT node
        select_node = query_ast if isinstance(query_ast, exp.Select) else query_ast.find(exp.Select)
        if not select_node: return False

        # if the expression IS an Alias (e.g., column AS name), validation fails
        for expression in select_node.expressions:
            if isinstance(expression, exp.Alias): return False
        return True

    @property
    def description(self) -> str:
        return "Columns in SELECT must NOT be renamed (must NOT use AS aliases)"



class RequireAlias(QueryConstraint):
    '''
    Requires that ALL columns in the main SELECT clause are renamed using an alias (AS).
    '''

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        # Find the main SELECT node
        select_node = query_ast if isinstance(query_ast, exp.Select) else query_ast.find(exp.Select)
        if not select_node: return False

        # If the expression is NOT an Alias, validation fails
        for expression in select_node.expressions:
            if not isinstance(expression, exp.Alias): return False
        return True

    @property
    def description(self) -> str:
        return "All columns in SELECT must be renamed using an alias (AS)"