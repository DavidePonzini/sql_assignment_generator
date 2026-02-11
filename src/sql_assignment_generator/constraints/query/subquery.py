from sql_assignment_generator.exceptions import ConstraintValidationError
from .base import QueryConstraint
from sqlscope import Query
from sqlglot import parse_one, exp

class NoSubquery(QueryConstraint):
    '''Requires the absence of subqueries in the SQL query.'''

    def validate(self, query: Query) -> bool:
        for select in query.selects:
            if len(select.subqueries) > 0:
                raise ConstraintValidationError(
                    "Subqueries were detected in the solution, but this exercise must be solved "
                    "without using any subqueries."
                )

    @property
    def description(self) -> str:
        return "Exercise must not require any subqueries."

class UnnestedSubqueries(QueryConstraint):
    '''Requires the presence of a certain number of unnested subqueries in the SQL query.'''
    def __init__(self, min_: int = 1, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_

    def validate(self, query: Query) -> bool:
        selects_collection = query.selects.values() if hasattr(query.selects, 'values') else query.selects 
        all_normalized_selects = []
        total_subqueries_found = 0

        for s in selects_collection:
            curr = s[1] if isinstance(s, tuple) else s
            if isinstance(curr, str): continue
            all_normalized_selects.append(curr)
            #cout total subqueryies found in the entire query (including nested ones)
            total_subqueries_found += len(curr.subqueries)

        #if there are more subqueries found than the number of main level selects, it means there is nesting
        main_subqueries_count = len(query.main_query.subqueries)
        
        if total_subqueries_found > main_subqueries_count:
            raise ConstraintValidationError(
                f"Nested subqueries detected (Total: {total_subqueries_found}, Main level: {main_subqueries_count}). "
                "All subqueries must be at the top level of the WHERE clause."
            )

        #if there are no subqueries at all, it fails the validation if min > 0
        unnested_subquery_counts = [len(select.subqueries) for select in all_normalized_selects]
        for count in unnested_subquery_counts:
            if self.max is None:
                if count >= self.min:
                    return
                continue
            if self.min <= count <= self.max:
                return
            continue

        raise ConstraintValidationError(
            f"Number of unnested subqueries is insufficient. Found counts per SELECT: {unnested_subquery_counts}. "
            f"Requirements: min={self.min}, max={self.max}"
        )

    @property
    def description(self) -> str:
        if self.max is None:
            return f'Exercise must require at least {self.min} unnested subqueries.'
        if self.min == self.max:
            return f'Exercise must require exactly {self.min} unnested subqueries.'
        return f'Exercise must require between {self.min} and {self.max} unnested subqueries.'

class Subqueries(QueryConstraint):
    '''Requires the presence of nested subqueries (a subquery inside another subquery).'''

    def __init__(self, min_: int = 1, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_

    def validate(self, query: Query) -> bool:
        ast = parse_one(query.sql)
        all_selects = list(ast.find_all(exp.Select))
        total_subqueries = len(all_selects) - 1

        if self.max is None:
            if total_subqueries >= self.min: 
                return
        elif self.min <= total_subqueries <= self.max:
            return

        raise ConstraintValidationError(
            f"Exercise does not have the required number of subqueries. "
            f"Found {total_subqueries}, but required min: {self.min}, max: {self.max if self.max else 'unlimited'}."
        )

    @property
    def description(self) -> str:
        if self.max is None: return f'Exercise must require at least {self.min} nested subqueries.'
        if self.min == self.max: return f'Exercise must require exactly {self.min} nested subqueries.'
        return f'Exercise must require between {self.min} and {self.max} nested subqueries.'