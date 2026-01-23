from collections import Counter
from .base import QueryConstraint
from sqlglot import Expression, exp
from sqlscope import Query
from sqlscope.catalog.constraint import ConstraintType



class RequireDuplicates(QueryConstraint):
    '''
    Require the query to return duplicate rows
    '''

    def validate(self, query: Query) -> bool:
        main_query = query.main_query

        output_constraints = main_query.output.unique_constraints

        return len(output_constraints) == 0
    
    
    @property
    def description(self) -> str:
        return 'The exercise must return duplicate rows, i.e., no unique/primary key on any columns in the SELECT clause, no DISTINCT keyword, and no grouping.'

class NoDuplicates(QueryConstraint):
    '''
    Require the query to return unique rows, even if DISTINCT is not used
    '''

    def validate(self, query: Query) -> bool:
        main_query = query.main_query

        output_constraints = main_query.output.unique_constraints

        other_constraints = [c for c in output_constraints if c.constraint_type != ConstraintType.DISTINCT]

        return len(other_constraints) > 0
    
    @property
    def description(self) -> str:
        return 'The exercise must select a unique/primary key, as well as any other columns in the SELECT clause, or grouping is applied.'

class RequireDistinct(QueryConstraint):
    '''
    Require the query to use the DISTINCT keyword to eliminate duplicate rows.
    This means that the query must return duplicate rows without DISTINCT, and return unique rows with DISTINCT.
    '''

    def validate(self, query: Query) -> bool:
        main_query = query.main_query

        output_constraints = main_query.output.unique_constraints

        has_distinct_constraint = any(c.constraint_type == ConstraintType.DISTINCT for c in output_constraints)

        return has_distinct_constraint

    @property
    def description(self) -> str:
        return 'The exercise must use the DISTINCT keyword to eliminate duplicate rows, ' \
        'meaning that, had DISTINCT not been used, the query would have returned duplicate rows.'