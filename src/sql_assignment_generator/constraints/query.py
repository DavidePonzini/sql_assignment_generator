from .base import BaseConstraint
from sqlglot import Expression

class HasWhereConstraint(BaseConstraint):
    '''Requires the presence of a WHERE clause in the SQL query.'''

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        where_clause = query_ast.args.get('where')

        return where_clause is not None
    
    @property
    def description(self) -> str:
        return 'Must contain a WHERE clause.'
    
class HasAggregationConstraint(BaseConstraint):
    '''Requires the presence of an aggregation function in the SQL query.'''

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        # TODO
        return True
    
    @property
    def description(self) -> str:
        return 'Must contain an aggregation function (e.g., COUNT, SUM, AVG).'
    
class HasSubqueryConstraint(BaseConstraint):
    '''Requires the presence of a subquery in the SQL query.'''

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        # TODO
        return True
    
    @property
    def description(self) -> str:
        return 'Must contain a subquery.'