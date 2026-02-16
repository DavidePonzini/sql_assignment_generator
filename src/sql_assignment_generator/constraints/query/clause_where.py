from collections import Counter
import random
from typing import Callable
from .base import QueryConstraint
from sqlscope import Query
from sqlglot import exp, parse_one
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
        ast = parse_one(query.sql)

        wheres = list(ast.find_all(exp.Where))
        ands = list(ast.find_all(exp.And))
        ors = list(ast.find_all(exp.Or))
        
        count = len(wheres) + len(ands) + len(ors)

        if self.max is None:
            if count < self.min:
                raise ConstraintValidationError(
                    f'Query must require at least {self.min} WHERE conditions, but only {count} were found.'
                )
            return
        
        if not (self.min <= count <= self.max):
            raise ConstraintValidationError(
                f'Query must require between {self.min} and {self.max} WHERE conditions, but found {count}.'
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
        ast = parse_one(query.sql)
        count = 0

        # look for all operator inside string
        for comparison in ast.find_all(tuple(self.allowed_operators)):
            if isinstance(comparison, (exp.Like, exp.ILike)):
                # elementi in right must be a string
                if comparison.expression.is_string:
                    count += 1
            else:
                # one of the sides must be a string
                left = comparison.left
                right = comparison.right
                is_left_str = isinstance(left, exp.Literal) and left.is_string
                is_right_str = isinstance(right, exp.Literal) and right.is_string

                if (is_left_str and not is_right_str) or (is_right_str and not is_left_str):
                    count += 1

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
        ast = parse_one(query.sql)
        count = 0

        # look for = e <> into query
        for comparison in ast.find_all((exp.EQ, exp.NEQ)):
            left = comparison.left
            right = comparison.right

            is_left_empty = isinstance(left, exp.Literal) and left.is_string and left.this == ""
            is_right_empty = isinstance(right, exp.Literal) and right.is_string and right.this == ""

            if (is_left_empty and not is_right_empty) or (is_right_empty and not is_left_empty):
                count += 1

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
        ast = parse_one(query.sql)
        count = 0

        # look for all 'IS'
        for is_node in ast.find_all(exp.Is):
            # verify NULL presence
            if isinstance(is_node.expression, exp.Null):
                # verify IS NULL (without NOT)
                is_not_parent = isinstance(is_node.parent, exp.Not)
                has_is_not_flag = is_node.args.get("is_not") is True
                
                if not is_not_parent and not has_is_not_flag:
                    count += 1

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
        ast = parse_one(query.sql)
        count = 0

        # look for all 'IS'
        for is_node in ast.find_all(exp.Is):
            # verify NULL presence
            if isinstance(is_node.expression, exp.Null):
                # verify IS NOT NULL
                is_not_parent = isinstance(is_node.parent, exp.Not)
                has_is_not_flag = is_node.args.get("is_not") is True
                
                if is_not_parent or has_is_not_flag: count += 1

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
        ast = parse_one(query.sql)
        
        # look for all node NOT inside query
        not_nodes = list(ast.find_all(exp.Not))
        
        # IS NOT NULL is attribute of exp.Is, controll also this
        is_not_null_count = 0
        for is_node in ast.find_all(exp.Is):
            if is_node.args.get("is_not"):
                is_not_null_count += 1
        
        count = len(not_nodes) + is_not_null_count

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
        ast = parse_one(query.sql)
        count = 0

        # Cerchiamo tutti i nodi EXISTS nell'intera query (Main + Subqueries)
        for exists_node in ast.find_all(exp.Exists):
            #verify that there isn't NOT (e.g. NOT EXISTS)
            if not isinstance(exists_node.parent, exp.Not):
                count += 1

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
        ast = parse_one(query.sql)
        count = 0

        # look for all EXIST
        for exists_node in ast.find_all(exp.Exists):
            # verify if EXIST has NOT
            p = exists_node.parent
            if isinstance(p, exp.Paren): p = p.parent
            if isinstance(p, exp.Not): count += 1

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
        math_operators = (
            exp.Add,  # +
            exp.Sub,  # -
            exp.Mul,  # *
            exp.Div,  # /
            exp.Mod   # %
        )

        ast = parse_one(query.sql)
        count = 0
        # look for all math operator in query
        for op in ast.find_all(math_operators):
            # verify if operator is in where clause
            if op.find_ancestor(exp.Where): count += 1

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

#REMOVED ERROR 56 NOT USED
# class ExistsNotExists_InNotIn(QueryConstraint):
#     '''
#     Requires the presence of a certain number of EXISTS/NOT EXISTS or IN/NOT IN operators in the WHERE clause of the SQL query.
#     '''

#     def __init__(self, min_pos: int = 1, min_neg: int = 1, max_pos: int | None = None, max_neg: int | None = None) -> None:
#         self.min_pos = min_pos
#         self.min_neg = min_neg
#         self.max_pos = max_pos
#         self.max_neg = max_neg

#     def validate(self, query: Query) -> None:
#         pos_count = 0
#         neg_count = 0

#         for select in query.main_query.selects:
#             where = select.where
#             if where is not None:
#                 # Look for EXISTS and IN operators
#                 for exists_node in where.find_all(exp.Exists):
#                     if not isinstance(exists_node.parent, exp.Not):
#                         pos_count += 1

#                 for in_node in where.find_all(exp.In):
#                     if not isinstance(in_node.parent, exp.Not):
#                         pos_count += 1

#                 # Look for NOT EXISTS and NOT IN operators
#                 for not_node in where.find_all(exp.Not):
#                     if isinstance(not_node.this, exp.Exists):
#                         neg_count += 1
#                     elif isinstance(not_node.this, exp.In):
#                         neg_count += 1

#         if self.max_pos is None:
#             pos_valid = pos_count >= self.min_pos
#         else:
#             pos_valid = self.min_pos <= pos_count <= self.max_pos

#         if self.max_neg is None:
#             neg_valid = neg_count >= self.min_neg
#         else:
#             neg_valid = self.min_neg <= neg_count <= self.max_neg

#         if not (pos_valid and neg_valid):
#             raise ConstraintValidationError(
#                 f'Query must require {self.description}. Found {pos_count} positive (EXISTS/IN) and {neg_count} negative (NOT EXISTS/NOT IN) operations.'
#             )
    
#     @property
#     def description(self) -> str:
#         pos_desc = ""
#         neg_desc = ""

#         if self.max_pos is None:
#             pos_desc = f'at least {self.min_pos} EXISTS or IN operations'
#         elif self.min_pos == self.max_pos:
#             pos_desc = f'exactly {self.min_pos} EXISTS or IN operations'
#         else:
#             pos_desc = f'between {self.min_pos} and {self.max_pos} EXISTS or IN operations'
#         if self.max_neg is None:
#             neg_desc = f'at least {self.min_neg} NOT EXISTS or NOT IN operations'
#         elif self.min_neg == self.max_neg:
#             neg_desc = f'exactly {self.min_neg} NOT EXISTS or NOT IN operations'
#         else:
#             neg_desc = f'between {self.min_neg} and {self.max_neg} NOT EXISTS or NOT IN operations'
#         return f'Exercise must require {pos_desc} and {neg_desc} on rows (WHERE conditions).'

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
        ast = parse_one(query.sql)
        individual_clause_counts = []
        
        for select in ast.find_all(exp.Select):
            where = select.args.get("where")
            having = select.args.get("having")

            if where is not None and having is not None:
                raise ConstraintValidationError(
                    "Query contains both WHERE and HAVING clauses in the same block. "
                    "This exercise requires using ONLY ONE of them."
                )

            for clause in [where, having]:
                if clause:
                    count = 1 + len(list(clause.find_all((exp.And, exp.Or))))
                    individual_clause_counts.append(count)

        found_valid = False
        for c in individual_clause_counts:
            if self.max is None:
                if c >= self.min: found_valid = True
            elif self.min <= c <= self.max:
                found_valid = True
            if found_valid: break

        if not found_valid:
            raise ConstraintValidationError(
                f'No valid WHERE or HAVING clause found with the required condition count ({self.min}-{self.max or "n"}).'
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
        ast = parse_one(query.sql)
        
        for select in ast.find_all(exp.Select):
            where = select.args.get("where")
            if where is None: continue

            column_counter = Counter()
            predicates = (exp.EQ, exp.NEQ, exp.GT, exp.LT, exp.GTE, exp.LTE, exp.Like, exp.ILike, exp.Between)
            
            for condition in where.find_all(predicates):
                if condition.find_ancestor(exp.Select) != select: continue
                
                column = condition.this
                if isinstance(column, exp.Column):
                    column_name = column.name.lower()
                    column_counter[column_name] += 1

                multiple_conditions_columns = sum(1 for count in column_counter.values() if count > 1)
                if multiple_conditions_columns >= self.min_columns: return
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
        ast = parse_one(query.sql)

        found_nodes = list(ast.find_all((exp.In, exp.Any, exp.All)))
        count = len(found_nodes)

        if count < self.min:
            error_msg = f'The query requires at least {self.min} operators among IN, ANY, or ALL, but only {count} were found.\n'
            if 'IN' in self.options:
                error_msg += '- Use IN to check if a value matches any value in a list or subquery.\n'
            if 'ANY' in self.options:
                error_msg += '- Use ANY to compare a value against at least one result from a subquery.\n'
            if 'ALL' in self.options:
                error_msg += '- Use ALL to compare a value against every result from a subquery.\n'

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
