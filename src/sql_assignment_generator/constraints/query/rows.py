from sql_assignment_generator.exceptions import ConstraintValidationError
from .base import QueryConstraint
from sqlscope import Query
from sqlscope.catalog.constraint import ConstraintType

class Duplicates(QueryConstraint):
    '''
    Require the query to return duplicate rows
    '''

    def validate(self, query: Query) -> bool:
        main_query = query.main_query
        curr_select = main_query[1] if isinstance(main_query, tuple) else main_query
        
        if curr_select.group_by and len(curr_select.group_by) > 0:
            raise ConstraintValidationError(self.description)
        
        output_constraints = main_query.output.unique_constraints

        if len(output_constraints) == 0: return
        raise ConstraintValidationError(
            f"The query is forced to return unique rows (Detected: {output_constraints}). "
            "The exercise requires a query that allows duplicate rows."
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
        curr_select = main_query[1] if isinstance(main_query, tuple) else main_query

        if curr_select.group_by and len(curr_select.group_by) > 0: return
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
        main_q = query.main_query
        curr_select = main_q[1] if isinstance(main_q, tuple) else main_q

        if curr_select.ast.args.get("distinct") is not None: return
        
        for expr in curr_select.ast.expressions:
            for node in expr.walk():
                if hasattr(node, 'key') and node.key == 'distinct': return

        raise ConstraintValidationError(
            "The DISTINCT keyword is missing. The exercise specifically requires explicit "
            "duplicate elimination using DISTINCT (either in SELECT or inside a function like COUNT)."
        )

    @property
    def description(self) -> str:
        return 'The exercise must use the DISTINCT keyword to eliminate duplicate rows, ' \
        'meaning that, had DISTINCT not been used, the query would have returned duplicate rows.'
