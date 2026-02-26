from .base import QueryConstraint
from sqlglot import exp
from sqlscope import Query
from ...exceptions import ConstraintValidationError
from ...translatable_text import TranslatableText

class NoOrderBy(QueryConstraint):
    '''Requires the absence of an ORDER BY clause.'''

    def validate(self, query: Query) -> None:
        for select in query.selects:
            if len(select.order_by) > 0:
                raise ConstraintValidationError(
                    TranslatableText(
                        'Exercise must not require ordering (i.e., no ORDER BY clause).',
                        it='L\'esercizio non deve richiedere ordinamento (i.e., nessuna clausola ORDER BY).'
                    )
                )
    
    @property
    def description(self) -> TranslatableText:
        return TranslatableText(
            'Exercise must not require ordering (i.e., no ORDER BY clause).',
            it='L\'esercizio non deve richiedere ordinamento (i.e., nessuna clausola ORDER BY).'
        )

class OrderBy(QueryConstraint):
    '''
    Requires the presence of an ORDER BY clause with a specific number of columns.
    Ordering can be ascending or descending.
    '''

    def __init__(self, min_: int = 1, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_

    def find_order_bys(self, query: Query) -> list[list[bool]]:
        '''
        Finds the number of columns in each ORDER BY clause within the query.

        Returns:
            A list of lists, where each inner list contains booleans indicating
            whether each column in the ORDER BY clause is ascending (True) or descending (False).
        '''

        order_bys: list[list[bool]] = []

        for select in query.selects:
            if len(select.order_by) == 0:
                continue

            order_by_columns: list[bool] = []
            for order in select.order_by:
                # Determine if the ordering is ascending (True) or descending (False)
                is_ascending = True
                if isinstance(order, exp.Ordered):
                    if order.args.get('desc', False):
                        is_ascending = False
                order_by_columns.append(is_ascending)

            order_bys.append(order_by_columns)

        return order_bys
    
    def validate(self, query: Query) -> None:
        order_bys = self.find_order_bys(query)

        for order_by in order_bys:
            count = len(order_by)

            if self.max is None:
                if count >= self.min:
                    return
                continue
            if self.min <= count <= self.max:
                return
            continue

        raise ConstraintValidationError(
            TranslatableText(
                f'Exercise does not satisfy the ORDER BY clause column count requirements.'
                f'ORDER BY clause column counts found: {[len(ob) for ob in order_bys]}, required min: {self.min}, required max: {self.max}',
                it=f'L\'esercizio non soddisfa i requisiti sul numero di colonne ORDER BY.'
                f'Conti delle colonne ORDER BY trovate: {[len(ob) for ob in order_bys]}, min richiesto: {self.min}, max richiesto: {self.max}'
            )
        )
    
    @property
    def description(self) -> TranslatableText:
        if self.max is None:
            return TranslatableText(
                f'Exercise must require ordering by at least {self.min} columns.',
                it=f'L\'esercizio deve richiedere ordinamento per almeno {self.min} colonne.'
            )
        elif self.min == self.max:
            return TranslatableText(
                f'Exercise must require ordering by exactly {self.min} columns.',
                it=f'L\'esercizio deve richiedere ordinamento per esattamente {self.min} colonne.'
            )
        else:
            return TranslatableText(
                f'Exercise must require ordering by between {self.min} and {self.max} columns.',
                it=f'L\'esercizio deve richiedere ordinamento tra {self.min} e {self.max} colonne.'
            )
        
class OrderByASC(OrderBy):
    '''
    Requires a certain number of columns in the ORDER BY clause to be in ascending order.
    '''

    def validate(self, query: Query) -> None:
        order_bys = self.find_order_bys(query)

        asc_counts: list[int] = []

        for order_by in order_bys:
            asc_count = sum(1 for is_asc in order_by if is_asc)
            asc_counts.append(asc_count)

            if self.max is None:
                if asc_count >= self.min:
                    return
                continue

            if self.min <= asc_count <= self.max:
                return
            continue

        error_msg = TranslatableText(
            f'Exercise does not satisfy the ORDER BY clause column count requirements.',
            it=f'L\'esercizio non soddisfa i requisiti sul numero di colonne ORDER BY.'
        )
        error_msg += TranslatableText(
            f' ORDER BY clause column counts found: {asc_counts}, required min: {self.min}',
            it=f' Conti delle colonne ORDER BY trovate: {asc_counts}, min richiesto: {self.min}'
        )
        if self.max is not None:
            error_msg += TranslatableText(
                f', required max: {self.max}.',
                it=f', max richiesto: {self.max}.'
            )
        error_msg += TranslatableText(
            ' Only ascending columns are counted.',
            it=' Solo le colonne in ordine crescente sono conteggiate.'
        )

        raise ConstraintValidationError(error_msg)
    
    @property
    def description(self) -> TranslatableText:
        if self.max is None:
            return TranslatableText(
                f'Exercise must require at least {self.min} columns in ORDER BY to be in ascending order.',
                it=f'L\'esercizio deve richiedere almeno {self.min} colonne in ORDER BY per essere in ordine crescente.'
            )
        elif self.min == self.max:
            return TranslatableText(
                f'Exercise must require exactly {self.min} columns in ORDER BY to be in ascending order.',
                it=f'L\'esercizio deve richiedere esattamente {self.min} colonne in ORDER BY per essere in ordine crescente.'
            )
        else:
            return TranslatableText(
                f'Exercise must require between {self.min} and {self.max} columns in ORDER BY to be in ascending order.',
                it=f'L\'esercizio deve richiedere tra {self.min} e {self.max} colonne in ORDER BY per essere in ordine crescente.'
            )
        
class OrderByDESC(OrderBy):
    '''
    Requires a certain number of columns in the ORDER BY clause to be in descending order.
    '''

    def validate(self, query: Query) -> None:
        order_bys = self.find_order_bys(query)
        desc_counts: list[int] = []

        for order_by in order_bys:
            desc_count = sum(1 for is_asc in order_by if not is_asc)
            desc_counts.append(desc_count)

            if self.max is None:
                if desc_count >= self.min:
                    return
                continue
            if self.min <= desc_count <= self.max:
                return
            continue

        error_msg = TranslatableText(
            f'Exercise does not satisfy the ORDER BY clause column count requirements.',
            it=f'L\'esercizio non soddisfa i requisiti sul numero di colonne ORDER BY.'
        )
        error_msg += TranslatableText(
            f' ORDER BY clause column counts found: {desc_counts}, required min: {self.min}',
            it=f' Conti delle colonne ORDER BY trovate: {desc_counts}, min richiesto: {self.min}'
        )
        if self.max is not None:
            error_msg += TranslatableText(
                f', required max: {self.max}.',
                it=f', max richiesto: {self.max}.'
            )
        error_msg += TranslatableText(
            ' Only descending columns are counted.',
            it=' Solo le colonne in ordine decrescente sono conteggiate.'
        )

        raise ConstraintValidationError(error_msg)
    
    @property
    def description(self) -> TranslatableText:
        if self.max is None:
            return TranslatableText(
                f'Exercise must require at least {self.min} columns in ORDER BY to be in descending order.',
                it=f'L\'esercizio deve richiedere almeno {self.min} colonne in ORDER BY per essere in ordine decrescente.'
            )
        elif self.min == self.max:
            return TranslatableText(
                f'Exercise must require exactly {self.min} columns in ORDER BY to be in descending order.',
                it=f'L\'esercizio deve richiedere esattamente {self.min} colonne in ORDER BY per essere in ordine decrescente.'
            )
        else:
            return TranslatableText(
                f'Exercise must require between {self.min} and {self.max} columns in ORDER BY to be in descending order.',
                it=f'L\'esercizio deve richiedere tra {self.min} e {self.max} colonne in ORDER BY per essere in ordine decrescente.'
            )