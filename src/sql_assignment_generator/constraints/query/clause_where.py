from collections import Counter
import random
from typing import Callable
from .base import QueryConstraint
from sqlscope import Query
from sqlglot import exp
from ...exceptions import ConstraintValidationError
from ...translatable_text import TranslatableText

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
            # avoid counting conditions in subqueries for this constraint,
            # since they will be counted separately when the validator visits those subqueries
            select = select.strip_subqueries()
            
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
                    TranslatableText(
                        f'Query must require at least {self.min} comparisons on rows (WHERE conditions), but only {count} were found.',
                        it=f'La query deve richiedere almeno {self.min} confronti sulle righe (condizioni WHERE), ma ne sono state trovate solo {count}.'
                    )
                )
            return
        
        if not (self.min <= count <= self.max):
            raise ConstraintValidationError(
                TranslatableText(
                    f'Query must require between {self.min} and {self.max} comparisons on rows (WHERE conditions), but found {count}.',
                    it=f'La query deve richiedere tra {self.min} e {self.max} confronti sulle righe (condizioni WHERE), ma ne sono state trovate {count}.'
                )
            )
                
    @property
    def description(self) -> TranslatableText:
        if self.max is None:
            return TranslatableText(
                f'Exercise must require at least one SELECT statement query with at least {self.min} comparisons on rows (WHERE conditions).',
                it=f'L’esercizio deve richiedere una query SELECT con almeno {self.min} confronti sulle righe (condizioni WHERE).'
            )
        if self.min == self.max:
            return TranslatableText(
                f'Exercise must require all SELECT statements to have exactly {self.min} comparisons on rows (WHERE conditions).',
                it=f'L’esercizio deve richiedere che tutte le query SELECT abbiano esattamente {self.min} confronti sulle righe (condizioni WHERE).'
            )
        return TranslatableText(
            f'Exercise must require all SELECT statements to have between {self.min} and {self.max} comparisons on rows (WHERE conditions).',
            it=f'L’esercizio deve richiedere che tutte le query SELECT abbiano tra {self.min} e {self.max} confronti sulle righe (condizioni WHERE).'
        )

# TODO: other classes
class StringComparison(QueryConstraint):
    '''
    Requires the presence of a certain number of WHERE conditions in the SQL query
    that compare string values.
    Only conditions using comparison operators in allowed_operators are considered.
    '''

    def __init__(
        self,
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
            # avoid counting conditions in subqueries for this constraint,
            # since they will be counted separately when the validator visits those subqueries
            select = select.strip_subqueries()

            where = select.where
            if where is not None:
                count = 0

                # LIKE requires the right side to be a string literal
                for like in where.find_all(tuple(op for op in (exp.Like, exp.ILike) if op in self.allowed_operators)): # type: ignore
                    right_side = like.expression
                    if isinstance(right_side, exp.Literal) and right_side.is_string:
                        count += 1

                # Other comparison operators can have string literals on either side
                for comparison in where.find_all(tuple(op for op in (exp.EQ, exp.NEQ, exp.GT, exp.LT, exp.GTE, exp.LTE) if op in self.allowed_operators)): # type: ignore
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
                    TranslatableText(
                        f'Query must require at least {self.min} string comparisons on rows (WHERE conditions), but only {count} were found.',
                        it=f'La query deve richiedere almeno {self.min} confronti di stringhe sulle righe (condizioni WHERE), ma ne sono state trovate solo {count}.'
                    )
                )
            return
        if not (self.min <= count <= self.max):
            raise ConstraintValidationError(
                TranslatableText(
                    f'Query must require between {self.min} and {self.max} string comparisons on rows (WHERE conditions), but found {count}.',
                    it=f'La query deve richiedere tra {self.min} e {self.max} confronti di stringhe sulle righe (condizioni WHERE), ma ne sono state trovate {count}.'
                )
            )
        
    @property
    def description(self) -> TranslatableText:
        operators_str = ', '.join([operator_to_string(op) for op in self.allowed_operators])

        if self.max is None:
            return TranslatableText(
                f'Exercise must require at least {self.min} string comparisons on rows (WHERE conditions) using any of the following operators: {operators_str}.',
                it=f'Esercizio deve richiedere almeno {self.min} confronti di stringhe sulle righe (condizioni WHERE) usando uno qualsiasi dei seguenti operatori: {operators_str}.'
            )
        if self.min == self.max:
            return TranslatableText(
                f'Exercise must require exactly {self.min} string comparisons on rows (WHERE conditions) using any of the following operators: {operators_str}.',
                it=f'Esercizio deve richiedere esattamente {self.min} confronti di stringhe sulle righe (condizioni WHERE) usando uno qualsiasi dei seguenti operatori: {operators_str}.'
            )
        return TranslatableText(
            f'Exercise must require between {self.min} and {self.max} string comparisons on rows (WHERE conditions) using any of the following operators: {operators_str}.',
            it=f'Esercizio deve richiedere tra {self.min} e {self.max} confronti di stringhe sulle righe (condizioni WHERE) usando uno qualsiasi dei seguenti operatori: {operators_str}.'
        )

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
            # avoid counting conditions in subqueries for this constraint,
            # since they will be counted separately when the validator visits those subqueries
            select = select.strip_subqueries()

            where = select.where
            if where is not None:
                count = 0

                # Look for '=' and '<>' comparisons to empty string
                for comparison in where.find_all((exp.EQ, exp.NEQ)): # type: ignore
                    left_side = comparison.this
                    right_side = comparison.expression

                    is_left_empty_string = isinstance(left_side, exp.Literal) and left_side.is_string and left_side.this == ''
                    is_right_empty_string = isinstance(right_side, exp.Literal) and right_side.is_string and right_side.this == ''

                    if is_left_empty_string and not is_right_empty_string:
                        count += 1
                    elif is_right_empty_string and not is_left_empty_string:
                        count += 1

                condition_count.append(count)

        count: int = sum(condition_count)
        if self.max is None:
            if count < self.min:
                raise ConstraintValidationError(
                    TranslatableText(
                        f'Query must require at least {self.min} comparisons to empty strings on rows (WHERE conditions), but only {count} were found.',
                        it=f'La query deve richiedere almeno {self.min} confronti a stringhe vuote sulle righe (condizioni WHERE), ma ne sono state trovate solo {count}.'
                    )
                )
            return
        if not (self.min <= count <= self.max):
            raise ConstraintValidationError(
                TranslatableText(
                    f'Query must require between {self.min} and {self.max} comparisons to empty strings on rows (WHERE conditions), but found {count}.',
                    it=f'La query deve richiedere tra {self.min} e {self.max} confronti a stringhe vuote sulle righe (condizioni WHERE), ma ne sono state trovate {count}.'
                )
            )
        
    @property
    def description(self) -> TranslatableText:
        if self.max is None:
            return TranslatableText(
                f'Exercise must require at least {self.min} comparisons to empty strings on rows (WHERE conditions) using "column = \'\'" or "column <> \'\'".',
                it=f'Esercizio deve richiedere almeno {self.min} confronti a stringhe vuote sulle righe (condizioni WHERE) usando "column = \'\'" o "column <> \'\'".'
            )
        if self.min == self.max:
            return TranslatableText(
                f'Exercise must require exactly {self.min} comparisons to empty strings on rows (WHERE conditions) using "column = \'\'" or "column <> \'\'".',
                it=f'Esercizio deve richiedere esattamente {self.min} confronti a stringhe vuote sulle righe (condizioni WHERE) usando "column = \'\'" o "column <> \'\'".'
            )
        return TranslatableText(
            f'Exercise must require between {self.min} and {self.max} comparisons to empty strings on rows (WHERE conditions) using "column = \'\'" or "column <> \'\'".',
            it=f'Esercizio deve richiedere tra {self.min} e {self.max} confronti a stringhe vuote sulle righe (condizioni WHERE) usando "column = \'\'" o "column <> \'\'".'
        )

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
            # avoid counting conditions in subqueries for this constraint,
            # since they will be counted separately when the validator visits those subqueries
            select = select.strip_subqueries()

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
                    TranslatableText(
                        f'Query must require at least {self.min} NULL checks on rows (WHERE conditions) using "IS NULL", but only {count} were found.',
                        it=f'La query deve richiedere almeno {self.min} controlli NULL sulle righe (condizioni WHERE) usando "IS NULL", ma ne sono stati trovati solo {count}.'
                    )
                )
            return
        if not (self.min <= count <= self.max):
            raise ConstraintValidationError(
                TranslatableText(
                    f'Query must require between {self.min} and {self.max} NULL checks on rows (WHERE conditions) using "IS NULL", but found {count}.',
                    it=f'La query deve richiedere tra {self.min} e {self.max} controlli NULL sulle righe (condizioni WHERE) usando "IS NULL", ma ne sono stati trovati {count}.'
                )
            )
        
    @property
    def description(self) -> TranslatableText:
        if self.max is None:
            return TranslatableText(
                f'Exercise must require at least {self.min} NULL checks on rows (WHERE conditions) using "IS NULL".',
                it=f'Esercizio deve richiedere almeno {self.min} controlli NULL sulle righe (condizioni WHERE) usando "IS NULL".'
            )
        if self.min == self.max:
            return TranslatableText(
                f'Exercise must require exactly {self.min} NULL checks on rows (WHERE conditions) using "IS NULL".',
                it=f'Esercizio deve richiedere esattamente {self.min} controlli NULL sulle righe (condizioni WHERE) usando "IS NULL".'
            )
        return TranslatableText(
            f'Exercise must require between {self.min} and {self.max} NULL checks on rows (WHERE conditions) using "IS NULL".',
            it=f'Esercizio deve richiedere tra {self.min} e {self.max} controlli NULL sulle righe (condizioni WHERE) usando "IS NULL".'
        )

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
            # avoid counting conditions in subqueries for this constraint,
            # since they will be counted separately when the validator visits those subqueries
            select = select.strip_subqueries()

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
                    TranslatableText(
                        f'Query must require at least {self.min} NOT NULL checks on rows (WHERE conditions) using "IS NOT NULL", but only {count} were found.',
                        it=f'La query deve richiedere almeno {self.min} controlli NOT NULL sulle righe (condizioni WHERE) usando "IS NOT NULL", ma ne sono stati trovati solo {count}.'
                    )
                )
            return
        if not (self.min <= count <= self.max):
            raise ConstraintValidationError(
                TranslatableText(
                    f'Query must require between {self.min} and {self.max} NOT NULL checks on rows (WHERE conditions) using "IS NOT NULL", but found {count}.',
                    it=f'La query deve richiedere tra {self.min} e {self.max} controlli NOT NULL sulle righe (condizioni WHERE) usando "IS NOT NULL", ma ne sono stati trovati {count}.'
                )
            )
        
    @property
    def description(self) -> TranslatableText:
        if self.max is None:
            return TranslatableText(
                f'Exercise must require at least {self.min} NOT NULL checks on rows (WHERE conditions) using "IS NOT NULL".',
                it=f'Esercizio deve richiedere almeno {self.min} controlli NOT NULL sulle righe (condizioni WHERE) usando "IS NOT NULL".'
            )
        if self.min == self.max:
            return TranslatableText(
                f'Exercise must require exactly {self.min} NOT NULL checks on rows (WHERE conditions) using "IS NOT NULL".',
                it=f'Esercizio deve richiedere esattamente {self.min} controlli NOT NULL sulle righe (condizioni WHERE) usando "IS NOT NULL".'
            )
        return TranslatableText(
            f'Exercise must require between {self.min} and {self.max} NOT NULL checks on rows (WHERE conditions) using "IS NOT NULL".',
            it=f'Esercizio deve richiedere tra {self.min} e {self.max} controlli NOT NULL sulle righe (condizioni WHERE) usando "IS NOT NULL".'
        )
    
class NoLike(QueryConstraint):
    '''Requires that there are no LIKE operators in the WHERE clause of the SQL query.'''

    def validate(self, query: Query) -> None:
        for select in query.main_query.selects:
            where = select.where
            if where is not None:
                # Look for LIKE comparisons
                like_nodes = list(where.find_all((exp.Like, exp.ILike))) # type: ignore
                if like_nodes:
                    raise ConstraintValidationError(
                        TranslatableText(
                            'Query must not require the use of LIKE operations on rows (WHERE conditions).',
                            it='La query non deve richiedere l\'uso di operazioni LIKE sulle righe (condizioni WHERE).'
                        )
                    )
    
    @property
    def description(self) -> TranslatableText:
        return TranslatableText(
            'Exercise must not require the use of LIKE operations on rows (WHERE conditions).',
            it='Esercizio non deve richiedere l\'uso di operazioni LIKE sulle righe (condizioni WHERE).'
        )

class Not(QueryConstraint):
    '''Requires the presence of a certain number of NOT operators in the WHERE clause of the SQL query.'''

    def __init__(self, min_: int = 1, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_

    def validate(self, query: Query) -> None:
        condition_count: list[int] = []

        for select in query.main_query.selects:
            # avoid counting NOT operators in subqueries for this constraint,
            # since they will be counted separately when the validator visits those subqueries
            select = select.strip_subqueries()
                
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
                    TranslatableText(
                        f'Query must require at least {self.min} NOT operations on rows (WHERE conditions), but only {count} were found.',
                        it=f'La query deve richiedere almeno {self.min} operazioni NOT sulle righe (condizioni WHERE), ma ne sono state trovate solo {count}.'
                    )
                )
            return
        if not (self.min <= count <= self.max):
            raise ConstraintValidationError(
                TranslatableText(
                    f'Query must require between {self.min} and {self.max} NOT operations on rows (WHERE conditions), but found {count}.',
                    it=f'La query deve richiedere tra {self.min} e {self.max} operazioni NOT sulle righe (condizioni WHERE), ma ne sono state trovate {count}.'
                )
            )
        
    @property
    def description(self) -> TranslatableText:
        if self.max is None:
            return TranslatableText(
                f'Exercise must require at least {self.min} NOT operations on rows (WHERE conditions).',
                it=f'Esercizio deve richiedere almeno {self.min} operazioni NOT sulle righe (condizioni WHERE).'
            )
        if self.min == self.max:
            return TranslatableText(
                f'Exercise must require exactly {self.min} NOT operations on rows (WHERE conditions).',
                it=f'Esercizio deve richiedere esattamente {self.min} operazioni NOT sulle righe (condizioni WHERE).'
            )
        return TranslatableText(
            f'Exercise must require between {self.min} and {self.max} NOT operations on rows (WHERE conditions).',
            it=f'Esercizio deve richiedere tra {self.min} e {self.max} operazioni NOT sulle righe (condizioni WHERE).'
        )
    
class Exists(QueryConstraint):
    '''Requires the presence of a certain number of EXIST operators in the WHERE clause of the SQL query.'''

    def __init__(self, min_: int = 1, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_

    def validate(self, query: Query) -> None:
        condition_count: list[int] = []

        for select in query.main_query.selects:
            # avoid counting NOT operators in subqueries for this constraint,
            # since they will be counted separately when the validator visits those subqueries
            select = select.strip_subqueries()
            
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
                    TranslatableText(
                        f'Query must require at least {self.min} EXIST operations on rows (WHERE conditions). NOT EXIST are not counted.',
                        it=f'La query deve richiedere almeno {self.min} operazioni EXIST sulle righe (condizioni WHERE). NOT EXIST non sono conteggiate.'
                    )
                )
            return
        if not (self.min <= count <= self.max):
            raise ConstraintValidationError(
                TranslatableText(
                    f'Query must require between {self.min} and {self.max} EXIST operations on rows (WHERE conditions). NOT EXIST are not counted.',
                    it=f'La query deve richiedere tra {self.min} e {self.max} operazioni EXIST sulle righe (condizioni WHERE). NOT EXIST non sono conteggiate.'
                )
            )
        
    @property
    def description(self) -> TranslatableText:
        if self.max is None:
            return TranslatableText(
                f'Exercise must require at least {self.min} EXIST operations on rows (WHERE conditions). NOT EXIST are not counted.',
                it=f'Esercizio deve richiedere almeno {self.min} operazioni EXIST sulle righe (condizioni WHERE). NOT EXIST non sono conteggiate.'
            )
        if self.min == self.max:
            return TranslatableText(
                f'Exercise must require exactly {self.min} EXIST operations on rows (WHERE conditions). NOT EXIST are not counted.',
                it=f'Esercizio deve richiedere esattamente {self.min} operazioni EXIST sulle righe (condizioni WHERE). NOT EXIST non sono conteggiate.'
            )
        return TranslatableText(
            f'Exercise must require between {self.min} and {self.max} EXIST operations on rows (WHERE conditions). NOT EXIST are not counted.',
            it=f'Esercizio deve richiedere tra {self.min} e {self.max} operazioni EXIST sulle righe (condizioni WHERE). NOT EXIST non sono conteggiate.'
        )

class NotExist(QueryConstraint):
    '''Requires the presence of a certain number of NOT EXIST operators in the WHERE clause of the SQL query.'''

    def __init__(self, min_: int = 1, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_

    def validate(self, query: Query) -> None:
        condition_count: list[int] = []

        for select in query.main_query.selects:
            # avoid counting NOT operators in subqueries for this constraint,
            # since they will be counted separately when the validator visits those subqueries
            select = select.strip_subqueries()
            
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
                    TranslatableText(
                        f'Query must require at least {self.min} NOT EXIST operations on rows (WHERE conditions).',
                        it=f'La query deve richiedere almeno {self.min} operazioni NOT EXIST sulle righe (condizioni WHERE).'
                    )
                )
            return
        if not (self.min <= count <= self.max):
            raise ConstraintValidationError(
                TranslatableText(
                    f'Query must require between {self.min} and {self.max} NOT EXIST operations on rows (WHERE conditions).',
                    it=f'La query deve richiedere tra {self.min} e {self.max} operazioni NOT EXIST sulle righe (condizioni WHERE).'
                )
            )
        
    @property
    def description(self) -> TranslatableText:
        if self.max is None:
            return TranslatableText(
                f'Exercise must require at least {self.min} NOT EXIST operations on rows (WHERE conditions).',
                it=f'Esercizio deve richiedere almeno {self.min} operazioni NOT EXIST sulle righe (condizioni WHERE).'
            )
        if self.min == self.max:
            return TranslatableText(
                f'Exercise must require exactly {self.min} NOT EXIST operations on rows (WHERE conditions).',
                it=f'Esercizio deve richiedere esattamente {self.min} operazioni NOT EXIST sulle righe (condizioni WHERE).'
            )
        return TranslatableText(
            f'Exercise must require between {self.min} and {self.max} NOT EXIST operations on rows (WHERE conditions).',
            it=f'Esercizio deve richiedere tra {self.min} e {self.max} operazioni NOT EXIST sulle righe (condizioni WHERE).'
        )

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
            # avoid counting NOT operators in subqueries for this constraint,
            # since they will be counted separately when the validator visits those subqueries
            select = select.strip_subqueries()
            
            where = select.where
            if where is not None:
                count = 0

                # Look for mathematical comparison operators
                for math_op in where.find_all(math_operators): # type: ignore
                    count += 1

                condition_count.append(count)

        count: int = sum(condition_count)
        if self.max is None:
            if count < self.min:
                raise ConstraintValidationError(
                    TranslatableText(
                        f'Query must require at least {self.min} mathematical operations (i.e. +, -, *, /, %) on rows (WHERE conditions).',
                        it=f'La query deve richiedere almeno {self.min} operazioni matematiche (i.e. +, -, *, /, %) sulle righe (condizioni WHERE).'
                    )
                )
            return
        if not (self.min <= count <= self.max):
            raise ConstraintValidationError(
                TranslatableText(
                    f'Query must require between {self.min} and {self.max} mathematical operations (i.e. +, -, *, /, %) on rows (WHERE conditions).',
                    it=f'La query deve richiedere tra {self.min} e {self.max} operazioni matematiche (i.e. +, -, *, /, %) sulle righe (condizioni WHERE).'
                )
            )
        
    @property
    def description(self) -> TranslatableText:
        if self.max is None:
            return TranslatableText(
                f'Exercise must require at least {self.min} mathematical operations (i.e. +, -, *, /, %) on rows (WHERE conditions).',
                it=f'Esercizio deve richiedere almeno {self.min} operazioni matematiche (i.e. +, -, *, /, %) sulle righe (condizioni WHERE).'
            )
        if self.min == self.max:
            return TranslatableText(
                f'Exercise must require exactly {self.min} mathematical operations (i.e. +, -, *, /, %) on rows (WHERE conditions).',
                it=f'Esercizio deve richiedere esattamente {self.min} operazioni matematiche (i.e. +, -, *, /, %) sulle righe (condizioni WHERE).'
            )
        return TranslatableText(
            f'Exercise must require between {self.min} and {self.max} mathematical operations (i.e. +, -, *, /, %) on rows (WHERE conditions).',
            it=f'Esercizio deve richiedere tra {self.min} e {self.max} operazioni matematiche (i.e. +, -, *, /, %) sulle righe (condizioni WHERE).'
        )

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
            # avoid counting NOT operators in subqueries for this constraint,
            # since they will be counted separately when the validator visits those subqueries
            select = select.strip_subqueries()
            
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
                TranslatableText(
                    f'Query must require {self.description}. Found {pos_count} positive (EXISTS/IN) and {neg_count} negative (NOT EXISTS/NOT IN) operations.',
                    it=f'La query deve richiedere {self.description}. Trovate {pos_count} operazioni positive (EXISTS/IN) e {neg_count} operazioni negative (NOT EXISTS/NOT IN).'
                )
            )
    
    @property
    def description(self) -> TranslatableText:
        pos_desc = ''
        neg_desc = ''

        if self.max_pos is None:
            pos_desc = TranslatableText(
                f'at least {self.min_pos} EXISTS or IN operations',
                it=f'almeno {self.min_pos} operazioni EXISTS o IN'
            )
        elif self.min_pos == self.max_pos:
            pos_desc = TranslatableText(
                f'exactly {self.min_pos} EXISTS or IN operations',
                it=f'esattamente {self.min_pos} operazioni EXISTS o IN'
            )
        else:
            pos_desc = TranslatableText(
                f'between {self.min_pos} and {self.max_pos} EXISTS or IN operations',
                it=f'compresi tra {self.min_pos} e {self.max_pos} operazioni EXISTS o IN'
            )
        if self.max_neg is None:
            neg_desc = TranslatableText(
                f'at least {self.min_neg} NOT EXISTS or NOT IN operations',
                it=f'almeno {self.min_neg} operazioni NOT EXISTS o NOT IN'
            )
        elif self.min_neg == self.max_neg:
            neg_desc = TranslatableText(
                f'exactly {self.min_neg} NOT EXISTS or NOT IN operations',
                it=f'esattamente {self.min_neg} operazioni NOT EXISTS o NOT IN'
            )
        else:
            neg_desc = TranslatableText(
                f'between {self.min_neg} and {self.max_neg} NOT EXISTS or NOT IN operations',
                it=f'tra {self.min_neg} e {self.max_neg} operazioni NOT EXISTS o NOT IN'
            )

        return TranslatableText(
            f'Exercise must require {pos_desc} and {neg_desc} on rows (WHERE conditions).',
            it=f'L\'esercizio deve richiedere {pos_desc} e {neg_desc} sulle righe (condizioni WHERE).'
        )

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
            # avoid counting NOT operators in subqueries for this constraint,
            # since they will be counted separately when the validator visits those subqueries
            select = select.strip_subqueries()
            
            where = select.where
            if where is None:
                continue

            for like in where.find_all((exp.Like, exp.ILike)): # type: ignore
                right_side = like.expression
                if isinstance(right_side, exp.Literal) and right_side.is_string:
                    literal_value = right_side.this

                    # Check if it contains all required characters with required counts
                    literal_counter = Counter(literal_value)
                    wildcard_status[literal_value] = all(literal_counter[char] >= count for char, count in self.required_characters.items())

        valid_wildcard_count = sum(1 for is_valid in wildcard_status.values() if is_valid)
        if valid_wildcard_count < self.min:
            raise ConstraintValidationError(
                TranslatableText(
                    f'Query must require at least {self.min} LIKE operations on rows (WHERE conditions) to contain the following wildcard characters with required counts: {self.required_characters}.'
                    f' Wildcards found and their validity: {wildcard_status}',
                    it=f'La query deve richiedere almeno {self.min} operazioni LIKE sulle righe (condizioni WHERE) per contenere i seguenti caratteri jolly con i conteggi richiesti: {self.required_characters}.'
                    f' Caratteri jolly trovati e la loro validità: {wildcard_status}'
                )
            )

    @property
    def description(self) -> TranslatableText:
        return TranslatableText(
            f'Exercise must require at least {self.min} LIKE operations on rows (WHERE conditions) to contain the following wildcard characters with required counts: {self.required_characters}.',
            it=f'L\'esercizio deve richiedere almeno {self.min} operazioni LIKE sulle righe (condizioni WHERE) per contenere i seguenti caratteri jolly con i conteggi richiesti: {self.required_characters}.'
        )

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
            # avoid counting NOT operators in subqueries for this constraint,
            # since they will be counted separately when the validator visits those subqueries
            select = select.strip_subqueries()
            
            where = select.where
            if where is not None:
                for like in where.find_all((exp.Like, exp.ILike)): # type: ignore
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
                                TranslatableText(
                                    'All LIKE operations on rows (WHERE conditions) must contain wildcards.',
                                    it='Tutte le operazioni LIKE sulle righe (condizioni WHERE) devono contenere caratteri jolly.'
                                )
                            )
                            
                        # Calculate length excluding special characters
                        length = sum(1 for char in literal_value if char not in special_characters)
                        wildcard_lengths[literal_value] = length

        if not wildcard_lengths:
            raise ConstraintValidationError(
                TranslatableText(
                    'Exercise must require all LIKE operations on rows (WHERE conditions) to contain wildcards. None were found.',
                    it='L\'esercizio deve richiedere tutte le operazioni LIKE sulle righe (condizioni WHERE) per contenere caratteri jolly. Nessuno è stato trovato.'
                )
            )

        for length in wildcard_lengths.values():                        
            if length < self.min:
                raise ConstraintValidationError(
                    TranslatableText(
                        f'All LIKE operations on rows (WHERE conditions) must have wildcards with at least {self.min} non-special characters. Wildcards found and their lengths: {wildcard_lengths}',
                        it=f'Tutte le operazioni LIKE sulle righe (condizioni WHERE) devono avere caratteri jolly con almeno {self.min} caratteri non speciali. Caratteri jolly trovati e loro lunghezze: {wildcard_lengths}'
                    )
                )
            if self.max is not None and length > self.max:
                raise ConstraintValidationError(
                    TranslatableText(
                        f'All LIKE operations on rows (WHERE conditions) must have wildcards with at most {self.max} non-special characters. Wildcards found and their lengths: {wildcard_lengths}',
                        it=f'Tutte le operazioni LIKE sulle righe (condizioni WHERE) devono avere caratteri jolly con al massimo {self.max} caratteri non speciali. Caratteri jolly trovati e loro lunghezze: {wildcard_lengths}'
                    )
                )
    @property
    def description(self) -> TranslatableText:
        if self.max is None:
            return TranslatableText(
                f'Exercise must require all LIKE operations on rows (WHERE conditions) to have wildcards with at least {self.min} non-special characters.',
                it=f'L\'esercizio deve richiedere tutte le operazioni LIKE sulle righe (condizioni WHERE) per avere caratteri jolly con almeno {self.min} caratteri non speciali.'
            )
        if self.min == self.max:
            return TranslatableText(
                f'Exercise must require all LIKE operations on rows (WHERE conditions) to have wildcards with exactly {self.min} non-special characters.',
                it=f'L\'esercizio deve richiedere tutte le operazioni LIKE sulle righe (condizioni WHERE) per avere caratteri jolly con esattamente {self.min} caratteri non speciali.'
            )
        return TranslatableText(
            f'Exercise must require all LIKE operations on rows (WHERE conditions) to have wildcards with between {self.min} and {self.max} non-special characters.',
            it=f'L\'esercizio deve richiedere tutte le operazioni LIKE sulle righe (condizioni WHERE) per avere caratteri jolly con tra {self.min} e {self.max} caratteri non speciali.'
        )

class MultipleConditionsOnSameColumn(QueryConstraint):
    '''Requires multiple conditions on the same column in the WHERE clause of the SQL query.'''

    def __init__(self, min_columns: int = 1) -> None:
        self.min_columns = min_columns

    def validate(self, query: Query) -> None:
        for select in query.main_query.selects:
            # avoid counting NOT operators in subqueries for this constraint,
            # since they will be counted separately when the validator visits those subqueries
            select = select.strip_subqueries()
            
            where = select.where
            if where is not None:
                column_counter = Counter()

                for condition in where.find_all((exp.EQ, exp.NEQ, exp.GT, exp.LT, exp.GTE, exp.LTE, exp.Like, exp.ILike, exp.Between)): # type: ignore
                    column = condition.this
                    if isinstance(column, exp.Column):
                        column_name = column.sql()
                        column_counter[column_name] += 1

                multiple_conditions_columns = sum(1 for count in column_counter.values() if count > 1)
                if multiple_conditions_columns >= self.min_columns:
                    return
        raise ConstraintValidationError(
            TranslatableText(
                f'Query must require at least {self.min_columns} columns to have multiple conditions on the same column in a single WHERE clause.',
                it=f'La query deve richiedere almeno {self.min_columns} colonne con più condizioni sulla stessa colonna in una singola clausola WHERE.'
            )
        )

    @property
    def description(self) -> TranslatableText:
        return TranslatableText(
            f'Exercise must require at least {self.min_columns} columns to have multiple conditions on the same column in a single WHERE clause.',
            it=f'Esercizio deve richiedere almeno {self.min_columns} colonne con più condizioni sulla stessa colonna in una singola clausola WHERE.'
        )

class InAnyAll(QueryConstraint):
    '''
    Requires the presence of a certain number of IN, ANY, or ALL operators in the SQL query.
    '''
    def __init__(self, min_: int = 1) -> None:
        self.min = min_
        self.options = random.sample(
            ['IN', 'ANY', 'ALL'],
            k=min(self.min, 3)
        )

    def validate(self, query: 'Query') -> None:
        count = 0

        for select in query.main_query.selects:
            # avoid counting NOT operators in subqueries for this constraint,
            # since they will be counted separately when the validator visits those subqueries
            select = select.strip_subqueries()

            if select.ast is None:
                # bogus SELECT, created by strip_subqueries - it has no AST
                continue
            
            exps = select.ast.find_all((exp.In, exp.Any, exp.All)) # type: ignore
            count += len(list(exps))

        import dav_tools
        dav_tools.messages.debug(count)

        if count < self.min:
            error_msg = TranslatableText()
            if 'IN' in self.options:
                error_msg += TranslatableText(
                    'Exercise must require selecting rows where a particular column is equal to one value of a subquery (IN).',
                    it='Esercizio deve richiedere la selezione di righe dove una particolare colonna è uguale a un valore di una sottosql (IN).'
                )
            if 'ANY' in self.options:
                error_msg += TranslatableText(
                    'Exercise must require selecting rows with a particular column higher/lower than at least one value in a subquery (ANY).',
                    it='Esercizio deve richiedere la selezione di righe con una particolare colonna maggiore/minore rispetto ad almeno un valore in una sottosql (ANY).'
                )
            if 'ALL' in self.options:
                error_msg += TranslatableText(
                    'Exercise must require selecting the rows with the highest/lowest value of particular column (ALL).',
                    it='Esercizio deve richiedere la selezione delle righe con il valore più alto/più basso di una particolare colonna (ALL).'
                )

            raise ConstraintValidationError(error_msg.strip())
    @property
    def description(self) -> TranslatableText:
        descriptions = {
            # col IN (subquery)
            'IN': TranslatableText(
                'The query must select rows where a particular column is equal to one value of a subquery.',
                it='La query deve selezionare righe dove una particolare colonna è uguale a un valore di una sottosql.'
            ),
            
            # col > ANY (subquery) | col < ANY (subquery)
            'ANY': TranslatableText(
                'The query must select rows with a particular column higher/lower than at least one value in a subquery.',
                it='La query deve selezionare righe con una particolare colonna maggiore/minore rispetto ad almeno un valore in una sottosql.'
            ),
            
            # col >= ALL (subquery) | col <= ALL (subquery)
            'ALL': TranslatableText(
                'The query must select the rows with the highest/lowest value of particular column.',
                it='La query deve selezionare le righe con il valore più alto/più basso di una particolare colonna.'
            ),
        }

        selected_constraints = TranslatableText()
        
        for option in self.options:
            selected_constraints += descriptions[option]
            selected_constraints += TranslatableText('\n', it='\n')     # must add a NL for each language
        
        return selected_constraints.strip()
