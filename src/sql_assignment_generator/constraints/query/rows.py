from sql_assignment_generator.exceptions import ConstraintValidationError
from .base import QueryConstraint
from sqlglot import Expression, exp
from sqlscope import Query
from sqlscope.catalog.constraint import ConstraintType

class Duplicates(QueryConstraint):
    '''
    Require the query to return duplicate rows
    '''

    def validate(self, query: Query) -> bool:
        main_query = query.main_query

        output_constraints = main_query.output.unique_constraints

        if len(output_constraints) == 0: return
        raise ConstraintValidationError(
            f"The query is forced to return unique rows due to: {output_constraints}. "
            f"The exercise requires a query that allows duplicate rows (no PK, no DISTINCT, no Group By)."
        )
    
    
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

        if len(other_constraints) > 0: return
        raise ConstraintValidationError(
            f"The query results are not guaranteed to be unique. To satisfy this constraint, "
            f"you must select a Primary Key/Unique column or apply grouping. "
            f"Current output constraints: {output_constraints}"
        )
    
    @property
    def description(self) -> str:
        return 'The exercise must select a unique/primary key, as well as any other columns in the SELECT clause, or grouping is applied.'

class Distinct(QueryConstraint):
    '''
    Require the query to use the DISTINCT keyword to eliminate duplicate rows.
    This means that the query must return duplicate rows without DISTINCT, and return unique rows with DISTINCT.
    '''

    def validate(self, query: Query) -> bool:
        main_query = query.main_query

        output_constraints = main_query.output.unique_constraints

        has_distinct_constraint = any(c.constraint_type == ConstraintType.DISTINCT for c in output_constraints)

        if has_distinct_constraint: return
        raise ConstraintValidationError(
            "The DISTINCT keyword is missing. The exercise specifically requires explicit "
            "duplicate elimination using DISTINCT."
        )

    @property
    def description(self) -> str:
        return 'The exercise must use the DISTINCT keyword to eliminate duplicate rows, ' \
        'meaning that, had DISTINCT not been used, the query would have returned duplicate rows.'
