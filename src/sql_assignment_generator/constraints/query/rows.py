from sql_assignment_generator.exceptions import ConstraintValidationError
from .base import QueryConstraint
from sqlglot import Expression, exp, parse_one
from sqlscope import Query
from sqlscope.catalog.constraint import ConstraintType

class Duplicates(QueryConstraint):
    '''
    Require the query to return duplicate rows
    '''

    def validate(self, query: Query) -> bool:
        ast = parse_one(query.sql)
        main_select = ast.find(exp.Select)
        if main_select:
            # there is DISTINCT
            if main_select.args.get("distinct") is not None:
                raise ConstraintValidationError(self.description)
            # there is GROUP BY
            if main_select.args.get("group") is not None:
                raise ConstraintValidationError(self.description)
    
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
        ast = parse_one(query.sql)
        main_select = ast.find(exp.Select)
        if main_select and main_select.args.get("group") is not None:
            return
        
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
        ast = parse_one(query.sql)

        #ptincipal SELECT clause of the query
        main_select = ast.find(exp.Select)
        if not main_select:
            return

        #check if DISTINCT is used in the main SELECT clause
        if main_select.args.get("distinct") is not None: return

        #look for DISTINCT in the expressions of the SELECT clause (e.g., COUNT(DISTINCT col))
        for expression in main_select.expressions:
            distinct_nodes = list(expression.find_all(exp.Distinct))
            if len(distinct_nodes) > 0: return

        main_q = query.main_query
        curr_q = main_q[1] if isinstance(main_q, tuple) else main_q
        
        if not isinstance(curr_q, str) and hasattr(curr_q, 'output'):
            output_constraints = curr_q.output.unique_constraints
            has_distinct = any(c.constraint_type == ConstraintType.DISTINCT for c in output_constraints)
            if has_distinct: return

        #no DISTINCT found
        raise ConstraintValidationError(
            "The DISTINCT keyword is missing. The exercise specifically requires explicit "
            "duplicate elimination using DISTINCT (either in SELECT or inside a function like COUNT)."
        )

    @property
    def description(self) -> str:
        return 'The exercise must use the DISTINCT keyword to eliminate duplicate rows, ' \
        'meaning that, had DISTINCT not been used, the query would have returned duplicate rows.'
