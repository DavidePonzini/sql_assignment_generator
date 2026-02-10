from collections import Counter
import random
from typing import Callable
from .base import QueryConstraint
from sqlscope import Query
from sqlglot import exp
from ...exceptions import ConstraintValidationError

def operator_to_string(op: type[exp.Predicate]) -> str:
    if op == exp.EQ:
        return '='
    elif op == exp.NEQ:
        return '<>'
    elif op == exp.GT:
        return '>'
    elif op == exp.LT:
        return '<'
    elif op == exp.GTE:
        return '>='
    elif op == exp.LTE:
        return '<='
    elif op == exp.Like:
        return 'LIKE'
    elif op == exp.ILike:
        return 'ILIKE'
    else:
        return ''

class Condition(QueryConstraint):
    '''
    Requires the presence of a certain number of WHERE conditions in the SQL query.
    Any kind of condition is accepted.
    '''

    def __init__(self, min_: int = 1, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_

    def validate(self, query: Query) -> None:
        condition_count: list[int] = []

        for select in query.main_query.selects:
            where = select.where
            if where is not None:
                count = 1  # Start with 1 for the initial condition
                count += len(list(where.find_all(exp.And)))
                count += len(list(where.find_all(exp.Or)))
                condition_count.append(count)

        count: int = sum(condition_count)
        if self.max is None:
            if count < self.min:
                raise ConstraintValidationError(
                    f'Query must require at least {self.min} comparisons on rows (WHERE conditions), but only {count} were found.'
                )
            return
        
        if not (self.min <= count <= self.max):
            raise ConstraintValidationError(
                f'Query must require between {self.min} and {self.max} comparisons on rows (WHERE conditions), but found {count}.'
            )
                
    @property
    def description(self) -> str:
        if self.max is None:
            return f'Exercise must require at least one SELECT statement query with at least {self.min} comparisons on rows (WHERE conditions).'
        if self.min == self.max:
            return f'Exercise must require all SELECT statements to have exactly {self.min} comparisons on rows (WHERE conditions).'
        return f'Exercise must require all SELECT statements to have between {self.min} and {self.max} comparisons on rows (WHERE conditions).'

# TODO: other classes
class StringComparison(QueryConstraint):
    '''
    Requires the presence of a certain number of WHERE conditions in the SQL query
    that compare string values.
    Only conditions using comparison operators in allowed_operators are considered.
    '''

    def __init__(self,
                 min_: int = 1,
                 max_: int | None = None,
                 *,
                 allowed_operators: list[type[exp.Predicate]] = [exp.Like, exp.ILike, exp.EQ, exp.NEQ, exp.GT, exp.LT, exp.GTE, exp.LTE],
        ) -> None:
        '''
        Requires the presence of a certain number of WHERE conditions in the SQL query
        that compare string values.
        Only conditions using comparison operators in allowed_operators are considered.

        :param min: Minimum number of string comparisons required.
        :param max: Maximum number of string comparisons allowed. If None, no upper limit.
        :param allowed_operators: List of comparison operator classes to consider.
        '''
        self.min = min_
        self.max = max_
        self.allowed_operators = allowed_operators

    def validate(self, query: Query) -> None:
        condition_count: list[int] = []

        for select in query.main_query.selects:
            where = select.where
            if where is not None:
                count = 0

                # LIKE requires the right side to be a string literal
                for like in where.find_all(tuple(op for op in (exp.Like, exp.ILike) if op in self.allowed_operators)):
                    right_side = like.expression
                    if isinstance(right_side, exp.Literal) and right_side.is_string:
                        count += 1

                # Other comparison operators can have string literals on either side
                for comparison in where.find_all(tuple(op for op in (exp.EQ, exp.NEQ, exp.GT, exp.LT, exp.GTE, exp.LTE) if op in self.allowed_operators)):
                    left_side = comparison.this
                    right_side = comparison.expression

                    # We also need to make sure that the two sides are not both literals
                    is_left_literal_string = isinstance(left_side, exp.Literal) and left_side.is_string
                    is_right_literal_string = isinstance(right_side, exp.Literal) and right_side.is_string

                    if is_left_literal_string and not is_right_literal_string:
                        count += 1
                    elif is_right_literal_string and not is_left_literal_string:
                        count += 1

                condition_count.append(count)

        count: int = sum(condition_count)
        if self.max is None:
            if count < self.min:
                raise ConstraintValidationError(
                    f'Query must require at least {self.min} string comparisons on rows (WHERE conditions), but only {count} were found.'
                )
            return
        if not (self.min <= count <= self.max):
            raise ConstraintValidationError(
                f'Query must require between {self.min} and {self.max} string comparisons on rows (WHERE conditions), but found {count}.'
            )
        
    @property
    def description(self) -> str:
        operators_str = ", ".join([operator_to_string(op) for op in self.allowed_operators])

        if self.max is None:
            return f'Exercise must require at least {self.min} string comparisons on rows (WHERE conditions) using any of the following operators: {operators_str}.'
        if self.min == self.max:
            return f'Exercise must require exactly {self.min} string comparisons on rows (WHERE conditions) using any of the following operators: {operators_str}.'
        return f'Exercise must require between {self.min} and {self.max} string comparisons on rows (WHERE conditions) using any of the following operators: {operators_str}.'

class EmptyStringComparison(QueryConstraint):
    '''
    Requires the presence of a certain number of WHERE conditions in the SQL query
    that compare to empty string values.
    Only conditions using '=' or '<>' operators are considered.
    '''

    def __init__(self, min_: int = 1, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_

    def validate(self, query: Query) -> None:
        condition_count: list[int] = []

        for select in query.main_query.selects:
            where = select.where
            if where is not None:
                count = 0

                # Look for '=' and '<>' comparisons to empty string
                for comparison in where.find_all((exp.EQ, exp.NEQ)):
                    left_side = comparison.this
                    right_side = comparison.expression

                    is_left_empty_string = isinstance(left_side, exp.Literal) and left_side.is_string and left_side.this == ""
                    is_right_empty_string = isinstance(right_side, exp.Literal) and right_side.is_string and right_side.this == ""

                    if is_left_empty_string and not is_right_empty_string:
                        count += 1
                    elif is_right_empty_string and not is_left_empty_string:
                        count += 1

                condition_count.append(count)

        count: int = sum(condition_count)
        if self.max is None:
            if count < self.min:
                raise ConstraintValidationError(
                    f'Query must require at least {self.min} comparisons to empty strings on rows (WHERE conditions), but only {count} were found.'
                )
            return
        if not (self.min <= count <= self.max):
            raise ConstraintValidationError(
                f'Query must require between {self.min} and {self.max} comparisons to empty strings on rows (WHERE conditions), but found {count}.'
            )
        
    @property
    def description(self) -> str:
        if self.max is None:
            return f'Exercise must require at least {self.min} comparisons to empty strings on rows (WHERE conditions) using "column = \'\'" or "column <> \'\'".'
        if self.min == self.max:
            return f'Exercise must require exactly {self.min} comparisons to empty strings on rows (WHERE conditions) using "column = \'\'" or "column <> \'\'".'
        return f'Exercise must require between {self.min} and {self.max} comparisons to empty strings on rows (WHERE conditions) using "column = \'\'" or "column <> \'\'".'

class NullComparison(QueryConstraint):
    '''
    Requires the presence of a certain number of WHERE conditions in the SQL query
    that check for NULL values.
    Only conditions using IS NULL are considered.
    '''

    def __init__(self, min_: int = 1, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_

    def validate(self, query: Query) -> None:
        condition_count: list[int] = []

        for select in query.main_query.selects:
            where = select.where
            if where is not None:
                count = 0

                # Look for IS NULL comparisons
                for is_null in where.find_all(exp.Is):
                    if isinstance(is_null.expression, exp.Null):
                        # Ensure it's not IS NOT NULL
                        if not isinstance(is_null.parent, exp.Not):
                            count += 1

                condition_count.append(count)

        count: int = sum(condition_count)
        if self.max is None:
            if count < self.min:
                raise ConstraintValidationError(
                    f'Query must require at least {self.min} NULL checks on rows (WHERE conditions) using "IS NULL", but only {count} were found.'
                )
            return
        if not (self.min <= count <= self.max):
            raise ConstraintValidationError(
                f'Query must require between {self.min} and {self.max} NULL checks on rows (WHERE conditions) using "IS NULL", but found {count}.'
            )
        
    @property
    def description(self) -> str:
        if self.max is None:
            return f'Exercise must require at least {self.min} NULL checks on rows (WHERE conditions) using "IS NULL".'
        if self.min == self.max:
            return f'Exercise must require exactly {self.min} NULL checks on rows (WHERE conditions) using "IS NULL".'
        return f'Exercise must require between {self.min} and {self.max} NULL checks on rows (WHERE conditions) using "IS NULL".'

class NotNullComparison(QueryConstraint):
    '''
    Requires the presence of a certain number of WHERE conditions in the SQL query
    that check for NOT NULL values.
    Only conditions using IS NOT NULL are considered.
    '''

    def __init__(self, min_: int = 1, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_

    def validate(self, query: Query) -> None:
        condition_count: list[int] = []

        for select in query.main_query.selects:
            where = select.where
            if where is not None:
                count = 0

                # Look for IS NOT NULL comparisons
                for is_null in where.find_all(exp.Is):
                    if isinstance(is_null.expression, exp.Null):
                        # Ensure it's IS NOT NULL
                        if isinstance(is_null.parent, exp.Not):
                            count += 1

                condition_count.append(count)

        count: int = sum(condition_count)
        if self.max is None:
            if count < self.min:
                raise ConstraintValidationError(
                    f'Query must require at least {self.min} NOT NULL checks on rows (WHERE conditions) using "IS NOT NULL", but only {count} were found.'
                )
            return
        if not (self.min <= count <= self.max):
            raise ConstraintValidationError(
                f'Query must require between {self.min} and {self.max} NOT NULL checks on rows (WHERE conditions) using "IS NOT NULL", but found {count}.'
            )
        
    @property
    def description(self) -> str:
        if self.max is None:
            return f'Exercise must require at least {self.min} NOT NULL checks on rows (WHERE conditions) using "IS NOT NULL".'
        if self.min == self.max:
            return f'Exercise must require exactly {self.min} NOT NULL checks on rows (WHERE conditions) using "IS NOT NULL".'
        return f'Exercise must require between {self.min} and {self.max} NOT NULL checks on rows (WHERE conditions) using "IS NOT NULL".'
    
class NoLike(QueryConstraint):
    '''Requires that there are no LIKE operators in the WHERE clause of the SQL query.'''

    def validate(self, query: Query) -> None:
        for select in query.main_query.selects:
            where = select.where
            if where is not None:
                # Look for LIKE comparisons
                like_nodes = list(where.find_all((exp.Like, exp.ILike)))
                if like_nodes:
                    raise ConstraintValidationError(
                        "Query must not require the use of LIKE operations on rows (WHERE conditions)."
                    )
    
    @property
    def description(self) -> str:
        return "Exercise must not require the use of LIKE operations on rows (WHERE conditions)."

class Not(QueryConstraint):
    '''Requires the presence of a certain number of NOT operators in the WHERE clause of the SQL query.'''

    def __init__(self, min_: int = 1, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_

    def validate(self, query: Query) -> None:
        condition_count: list[int] = []

        for select in query.main_query.selects:
            where = select.where
            if where is not None:
                count = 0

                # Look for NOT operators
                not_nodes = list(where.find_all(exp.Not))
                count += len(not_nodes)

                condition_count.append(count)

        count: int = sum(condition_count)
        if self.max is None:
            if count < self.min:
                raise ConstraintValidationError(
                    f'Query must require at least {self.min} NOT operations on rows (WHERE conditions), but only {count} were found.'
                )
            return
        if not (self.min <= count <= self.max):
            raise ConstraintValidationError(
                f'Query must require between {self.min} and {self.max} NOT operations on rows (WHERE conditions), but found {count}.'
            )
        
    @property
    def description(self) -> str:
        if self.max is None:
            return f'Exercise must require at least {self.min} NOT operations on rows (WHERE conditions).'
        if self.min == self.max:
            return f'Exercise must require exactly {self.min} NOT operations on rows (WHERE conditions).'
        return f'Exercise must require between {self.min} and {self.max} NOT operations on rows (WHERE conditions).'
    
class Exists(QueryConstraint):
    '''Requires the presence of a certain number of EXIST operators in the WHERE clause of the SQL query.'''

    def __init__(self, min_: int = 1, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_

    def validate(self, query: Query) -> None:
        condition_count: list[int] = []

        for select in query.main_query.selects:
            where = select.where
            if where is not None:
                count = 0

                # Look for EXIST operators
                for exists_node in where.find_all(exp.Exists):
                    # if parent isn't NOT
                    if not isinstance(exists_node.parent, exp.Not):
                        count += 1

                condition_count.append(count)

        count: int = sum(condition_count)
        if self.max is None:
            if count < self.min:
                raise ConstraintValidationError(
                    f'Query must require at least {self.min} EXIST operations on rows (WHERE conditions). NOT EXIST are not counted.'
                )
            return
        if not (self.min <= count <= self.max):
            raise ConstraintValidationError(
                f'Query must require between {self.min} and {self.max} EXIST operations on rows (WHERE conditions). NOT EXIST are not counted.'
            )
        
    @property
    def description(self) -> str:
        if self.max is None:
            return f'Exercise must require at least {self.min} EXIST operations on rows (WHERE conditions). NOT EXIST are not counted.'
        if self.min == self.max:
            return f'Exercise must require exactly {self.min} EXIST operations on rows (WHERE conditions). NOT EXIST are not counted.'
        return f'Exercise must require between {self.min} and {self.max} EXIST operations on rows (WHERE conditions). NOT EXIST are not counted.'

class NotExist(QueryConstraint):
    '''Requires the presence of a certain number of NOT EXIST operators in the WHERE clause of the SQL query.'''

    def __init__(self, min_: int = 1, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_

    def validate(self, query: Query) -> None:
        condition_count: list[int] = []

        for select in query.main_query.selects:
            where = select.where
            if where is not None:
                count = 0

                # Look for NOT EXIST operators
                for not_node in where.find_all(exp.Not):
                    if isinstance(not_node.this, exp.Exists):
                        count += 1

                condition_count.append(count)

        count: int = sum(condition_count)
        if self.max is None:
            if count < self.min:
                raise ConstraintValidationError(
                    f'Query must require at least {self.min} NOT EXIST operations on rows (WHERE conditions).'
                )
            return
        if not (self.min <= count <= self.max):
            raise ConstraintValidationError(
                f'Query must require between {self.min} and {self.max} NOT EXIST operations on rows (WHERE conditions).'
            )
        
    @property
    def description(self) -> str:
        if self.max is None:
            return f'Exercise must require at least {self.min} NOT EXIST operations on rows (WHERE conditions).'
        if self.min == self.max:
            return f'Exercise must require exactly {self.min} NOT EXIST operations on rows (WHERE conditions).'
        return f'Exercise must require between {self.min} and {self.max} NOT EXIST operations on rows (WHERE conditions).'

class MathOperators(QueryConstraint):
    '''Requires the presence of a certain number of mathematical operators in the WHERE clause of the SQL query.'''

    def __init__(self, min_: int = 1, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_

    def validate(self, query: Query) -> None:
        condition_count: list[int] = []

        math_operators = (
            exp.Add,  # +
            exp.Sub,  # -
            exp.Mul,  # *
            exp.Div,  # /
            exp.Mod   # %
        )

        for select in query.main_query.selects:
            where = select.where
            if where is not None:
                count = 0

                # Look for mathematical comparison operators
                for math_op in where.find_all(math_operators):
                    count += 1

                condition_count.append(count)

        count: int = sum(condition_count)
        if self.max is None:
            if count < self.min:
                raise ConstraintValidationError(
                    f'Query must require at least {self.min} mathematical operations (i.e. +, -, *, /, %) on rows (WHERE conditions).'
                )
            return
        if not (self.min <= count <= self.max):
            raise ConstraintValidationError(
                f'Query must require between {self.min} and {self.max} mathematical operations (i.e. +, -, *, /, %) on rows (WHERE conditions).'
            )
        
    @property
    def description(self) -> str:
        if self.max is None:
            return f'Exercise must require at least {self.min} mathematical operations (i.e. +, -, *, /, %) on rows (WHERE conditions).'
        if self.min == self.max:
            return f'Exercise must require exactly {self.min} mathematical operations (i.e. +, -, *, /, %) on rows (WHERE conditions).'
        return f'Exercise must require between {self.min} and {self.max} mathematical operations (i.e. +, -, *, /, %) on rows (WHERE conditions).'

class ExistsNotExists_InNotIn(QueryConstraint):
    '''
    Requires the presence of a certain number of EXISTS/NOT EXISTS or IN/NOT IN operators in the WHERE clause of the SQL query.
    '''

    def __init__(self, min_pos: int = 1, min_neg: int = 1, max_pos: int | None = None, max_neg: int | None = None) -> None:
        self.min_pos = min_pos
        self.min_neg = min_neg
        self.max_pos = max_pos
        self.max_neg = max_neg

    def validate(self, query: Query) -> None:
        pos_count = 0
        neg_count = 0

        for select in query.main_query.selects:
            where = select.where
            if where is not None:
                # Look for EXISTS and IN operators
                for exists_node in where.find_all(exp.Exists):
                    if not isinstance(exists_node.parent, exp.Not):
                        pos_count += 1

                for in_node in where.find_all(exp.In):
                    if not isinstance(in_node.parent, exp.Not):
                        pos_count += 1

                # Look for NOT EXISTS and NOT IN operators
                for not_node in where.find_all(exp.Not):
                    if isinstance(not_node.this, exp.Exists):
                        neg_count += 1
                    elif isinstance(not_node.this, exp.In):
                        neg_count += 1

        if self.max_pos is None:
            pos_valid = pos_count >= self.min_pos
        else:
            pos_valid = self.min_pos <= pos_count <= self.max_pos

        if self.max_neg is None:
            neg_valid = neg_count >= self.min_neg
        else:
            neg_valid = self.min_neg <= neg_count <= self.max_neg

        if not (pos_valid and neg_valid):
            raise ConstraintValidationError(
                f'Query must require {self.description}. Found {pos_count} positive (EXISTS/IN) and {neg_count} negative (NOT EXISTS/NOT IN) operations.'
            )
    
    @property
    def description(self) -> str:
        pos_desc = ""
        neg_desc = ""

        if self.max_pos is None:
            pos_desc = f'at least {self.min_pos} EXISTS or IN operations'
        elif self.min_pos == self.max_pos:
            pos_desc = f'exactly {self.min_pos} EXISTS or IN operations'
        else:
            pos_desc = f'between {self.min_pos} and {self.max_pos} EXISTS or IN operations'
        if self.max_neg is None:
            neg_desc = f'at least {self.min_neg} NOT EXISTS or NOT IN operations'
        elif self.min_neg == self.max_neg:
            neg_desc = f'exactly {self.min_neg} NOT EXISTS or NOT IN operations'
        else:
            neg_desc = f'between {self.min_neg} and {self.max_neg} NOT EXISTS or NOT IN operations'

        return f'Exercise must require {pos_desc} and {neg_desc} on rows (WHERE conditions).'

class WildcardCharacters(QueryConstraint):
    '''
    Requires for at least a certain amount of wildcards to have specific characters
    appear at least as many times as specified in the input string, regardless of position,
    in LIKE operations in the WHERE clause of the SQL query.
    '''

    def __init__(self, required_characters: str, min_: int = 1) -> None:
        self.min = min_
        self.required_characters: Counter[str] = Counter(required_characters)

    def validate(self, query: Query) -> None:
        wildcard_status: dict[str, bool] = {}
        '''True if the wildcard contains all required characters with required counts, False if it's an invalid wildcard.'''
        
        for select in query.main_query.selects:
            where = select.where
            if where is None:
                continue

            for like in where.find_all((exp.Like, exp.ILike)):
                right_side = like.expression
                if isinstance(right_side, exp.Literal) and right_side.is_string:
                    literal_value = right_side.this

                    # Check if it contains all required characters with required counts
                    literal_counter = Counter(literal_value)
                    wildcard_status[literal_value] = all(literal_counter[char] >= count for char, count in self.required_characters.items())

        valid_wildcard_count = sum(1 for is_valid in wildcard_status.values() if is_valid)
        if valid_wildcard_count < self.min:
            raise ConstraintValidationError(
                f'Query must require at least {self.min} LIKE operations on rows (WHERE conditions) to contain the following wildcard characters with required counts: {self.required_characters}.'
                f' Wildcards found and their validity: {wildcard_status}'
            )

    @property
    def description(self) -> str:
        return f'Exercise must require at least {self.min} LIKE operations on rows (WHERE conditions) to contain the following wildcard characters with required counts: {self.required_characters}.'

class WildcardLength(QueryConstraint):
    '''
    Requires all wildcards in the WHERE clause of the SQL query to have a minimum/maximum length, not counting special characters.
    '''

    def __init__(self, min_: int = 4, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_

    def validate(self, query: Query) -> None:
        special_characters = {'%', '_', '[', ']', '^', '-', '*', '+', '?', '(', ')', '{', '}'}
    
        wildcard_lengths: dict[str, int] = {}
    
        for select in query.main_query.selects:
            where = select.where
            if where is not None:
                for like in where.find_all((exp.Like, exp.ILike)):
                    right_side = like.expression
                    if isinstance(right_side, exp.Literal) and right_side.is_string:
                        literal_value = right_side.this

                        # Check if it contains special characters (i.e. is a valid wildcard)
                        no_wildcards: list[str] = []
                        for char in literal_value:
                            if char not in special_characters:
                                no_wildcards.append(char)
                        
                        if not any(char in special_characters for char in literal_value):
                            raise ConstraintValidationError(
                                "All LIKE operations on rows (WHERE conditions) must contain wildcards."
                            )
                            
                        # Calculate length excluding special characters
                        length = sum(1 for char in literal_value if char not in special_characters)
                        wildcard_lengths[literal_value] = length

        if not wildcard_lengths:
            raise ConstraintValidationError(
                "Exercise must require all LIKE operations on rows (WHERE conditions) to contain wildcards. None were found."
            )

        for length in wildcard_lengths.values():                        
            if length < self.min:
                raise ConstraintValidationError(
                    f'All LIKE operations on rows (WHERE conditions) must have wildcards with at least {self.min} non-special characters.'
                    f'Wildcards found and their lengths: {wildcard_lengths}'
                )
            if self.max is not None and length > self.max:
                raise ConstraintValidationError(
                    f'All LIKE operations on rows (WHERE conditions) must have wildcards with at most {self.max} non-special characters.'
                    f'Wildcards found and their lengths: {wildcard_lengths}'
                )
    @property
    def description(self) -> str:
        if self.max is None:
            return f'Exercise must require all LIKE operations on rows (WHERE conditions) to have wildcards with at least {self.min} non-special characters.'
        if self.min == self.max:
            return f'Exercise must require all LIKE operations on rows (WHERE conditions) to have wildcards with exactly {self.min} non-special characters.'
        return f'Exercise must require all LIKE operations on rows (WHERE conditions) to have wildcards with between {self.min} and {self.max} non-special characters.'

class Condition_WhereHaving(QueryConstraint):
    '''
    Requires the presence of a certain number of conditions in either WHERE or HAVING clauses of the SQL query.
    Any kind of condition is accepted.
    '''

    def __init__(self, min_: int = 1, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_

    def validate(self, query: Query) -> None:
        condition_count: list[int] = []

        for select in query.main_query.selects:
            where = select.where
            having = select.having
            total_conditions = 0

            if where is not None:
                count = 1  # Start with 1 for the initial condition
                count += len(list(where.find_all(exp.And)))
                count += len(list(where.find_all(exp.Or)))
                total_conditions += count

            if having is not None:
                count = 1  # Start with 1 for the initial condition
                count += len(list(having.find_all(exp.And)))
                count += len(list(having.find_all(exp.Or)))
                total_conditions += count

            if total_conditions > 0:
                condition_count.append(total_conditions)

        count: int = sum(condition_count)
        if self.max is None:
            if count < self.min:
                raise ConstraintValidationError(
                    f'Query must require at least {self.min} comparisons on rows (WHERE conditions) or groups (HAVING conditions), but only {count} were found.'
                )
            return
        if not (self.min <= count <= self.max):
            raise ConstraintValidationError(
                f'Query must require between {self.min} and {self.max} comparisons on rows (WHERE conditions) or groups (HAVING conditions), but found {count}.'
            )

    @property
    def description(self) -> str:
        if self.max is None:
            return f'Exercise must require at least {self.min} comparisons on rows (WHERE conditions) or groups (HAVING conditions).'
        if self.min == self.max:
            return f'Exercise must require exactly {self.min} comparisons on rows (WHERE conditions) or groups (HAVING conditions).'
        return f'Exercise must require between {self.min} and {self.max} comparisons on rows (WHERE conditions) or groups (HAVING conditions).'

class MultipleConditionsOnSameColumn(QueryConstraint):
    '''Requires multiple conditions on the same column in the WHERE clause of the SQL query.'''

    def __init__(self, min_columns: int = 1) -> None:
        self.min_columns = min_columns

    def validate(self, query: Query) -> None:
        for select in query.main_query.selects:
            where = select.where
            if where is not None:
                column_counter = Counter()

                for condition in where.find_all((exp.EQ, exp.NEQ, exp.GT, exp.LT, exp.GTE, exp.LTE, exp.Like, exp.ILike, exp.Between)):
                    column = condition.this
                    if isinstance(column, exp.Column):
                        column_name = column.sql()
                        column_counter[column_name] += 1

                multiple_conditions_columns = sum(1 for count in column_counter.values() if count > 1)
                if multiple_conditions_columns >= self.min_columns:
                    return
        raise ConstraintValidationError(
            f'Query must require at least {self.min_columns} columns to have multiple conditions on the same column in a single WHERE clause.'
        )

    @property
    def description(self) -> str:
        return f'Exercise must require at least {self.min_columns} columns to have multiple conditions on the same column in a single WHERE clause.'

class InAnyAll(QueryConstraint):
    '''
    Requires the presence of a certain number of IN, ANY, or ALL operators in the SQL query.
    '''
    def __init__(self, min_: int = 1 ) -> None:
        self.min = min_
        self.options = random.sample(
            ['IN', 'ANY', 'ALL'],
            k=min(self.min, 3)
        )

    def validate(self, query: 'Query') -> None:
        count = 0

        for select in query.main_query.selects:
            select = select.strip_subqueries()  # prevent double counting of subqueries

            exps = select.ast.find_all((exp.In, exp.Any, exp.All))
            count += len(list(exps))

        if count < self.min:
            error_msg = ''
            if 'IN' in self.options:
                error_msg += 'Exercise must require selecting rows where a particular column is equal to one value of a subquery (IN).\n'
            if 'ANY' in self.options:
                error_msg += 'Exercise must require selecting rows with a particular column higher/lower than at least one value in a subquery (ANY).\n'
            if 'ALL' in self.options:
                error_msg += 'Exercise must require selecting the rows with the highest/lowest value of particular column (ALL).\n'

            raise ConstraintValidationError(error_msg.strip())
    @property
    def description(self) -> str:
        descriptions = {
            # col IN (subquery)
            'IN': "The query must select rows where a particular column is equal to one value of a subquery (IN).",
            
            # col > ANY (subquery) | col < ANY (subquery)
            'ANY': "The query must select rows with a particular column higher/lower than at least one value in a subquery (ANY).",
            
            # col >= ALL (subquery) | col <= ALL (subquery)
            'ALL': "The query must select the rows with the highest/lowest value of particular column (ALL).",
        }

        selected_constraints = [descriptions[option] for option in self.options]        
        
        return '\n'.join(selected_constraints)
