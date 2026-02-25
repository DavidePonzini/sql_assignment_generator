from collections import Counter
from .base import QueryConstraint
from sqlglot import Expression, exp
from sqlscope import Query
from sqlscope.catalog.constraint import ConstraintType
from ...exceptions import ConstraintValidationError

class Duplicates(QueryConstraint):
    '''
    Require the query to return duplicate rows
    '''

    def validate(self, query: Query) -> None:
        main_query = query.main_query

        output = main_query.output
        output_constraints = output.unique_constraints

        if len(output_constraints) > 0:
            raise ConstraintValidationError(f'The exercise must return duplicate rows, but the query has unique constraints on the output columns. Current unique constraints: {output_constraints}')
    
    @property
    def description(self) -> str:
        return 'The exercise must return duplicate rows, i.e., no unique/primary key on any columns in the SELECT clause, no DISTINCT keyword, and no grouping.'

class NoDuplicates(QueryConstraint):
    '''
    Require the query to return unique rows, even if DISTINCT is not used
    '''

    def validate(self, query: Query) -> None:
        main_query = query.main_query

        output_constraints = main_query.output.unique_constraints

        other_constraints = [c for c in output_constraints if c.constraint_type != ConstraintType.DISTINCT]

        if len(other_constraints) == 0:
            raise ConstraintValidationError('The exercise must return unique rows, but the query has no unique constraints on the output columns (e.g. DISTINCT, GROUP BY, or selection of a primary key).}')
    
    @property
    def description(self) -> str:
        return 'The exercise must select a unique/primary key, as well as any other columns in the SELECT clause, or grouping is applied.'

class Distinct(QueryConstraint):
    '''
    Require the query to use the DISTINCT keyword to eliminate duplicate rows.
    This means that the query must return duplicate rows without DISTINCT, and return unique rows with DISTINCT.
    '''

    def validate(self, query: Query) -> None:
        main_query = query.main_query

        output_constraints = main_query.output.unique_constraints

        has_distinct_constraint = any(c.constraint_type == ConstraintType.DISTINCT for c in output_constraints)
        other_constraints = [c for c in output_constraints if c.constraint_type != ConstraintType.DISTINCT]

        if not has_distinct_constraint or len(other_constraints) > 0:
            raise ConstraintValidationError('The exercise must use the DISTINCT keyword to eliminate duplicate rows, but the query does not use DISTINCT. Without DISTINCT, the query would return duplicate rows, but with DISTINCT it returns unique rows.')

    @property
    def description(self) -> str:
        return 'The exercise must use the DISTINCT keyword to eliminate duplicate rows, ' \
        'meaning that, had DISTINCT not been used, the query would have returned duplicate rows.'
