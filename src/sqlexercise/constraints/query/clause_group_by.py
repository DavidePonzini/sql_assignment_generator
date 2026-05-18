from .base import QueryConstraint
from sqlscope import Query
from ...exceptions import ConstraintValidationError
from ...translatable_text import TranslatableText

class NoGroupBy(QueryConstraint):
    '''Requires the absence of a GROUP BY clause.'''

    def validate(self, query: Query) -> None:
        #look for node GROUP BY in query
        for select in query.selects:
            if len(select.group_by) > 0:
                raise ConstraintValidationError(
                    TranslatableText(
                        'Exercise must not contain a GROUP BY clause, but it does.',
                        it='L\'esercizio non deve contenere una clausola GROUP BY, ma lo fa.'
                    )
                )
    
    @property
    def description(self) -> TranslatableText:
        return TranslatableText(
            'Exercise must not require grouping (i.e., no GROUP BY clause).',
            it='L\'esercizio non deve richiedere raggruppamento (i.e., nessuna clausola GROUP BY).'
        )

class GroupBy(QueryConstraint):
    '''Requires the presence of a GROUP BY clause, optionally on a specified number of columns.'''

    def __init__(self, min_: int = 1, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_
    
    def validate(self, query: Query) -> None:
        # NOTE: in case multiple SELECTs (UNION/subqueries), the constraint is satisfied if ANY of them satisfy the constraint

        group_sizes: list[int] = []

        for select in query.selects:
            if len(select.group_by) == 0:
                continue
            group_sizes.append(len(select.group_by))

        # check if any group size satisfies the min/max condition
        for group_size in group_sizes:
            if self.max is None:
                if group_size >= self.min:
                    return
                continue
            if self.min <= group_size <= self.max:
                return
            continue

        raise ConstraintValidationError(
            TranslatableText(
                f'Exercise does not satisfy the GROUP BY column count requirements.'
                f'GROUP BY column counts found: {group_sizes}, required min: {self.min}, required max: {self.max}',
                it=f'L\'esercizio non soddisfa i requisiti sul numero di colonne GROUP BY.'
                f'Conti delle colonne GROUP BY trovate: {group_sizes}, min richiesto: {self.min}, max richiesto: {self.max}'
            )
        )

    @property
    def description(self) -> TranslatableText:
        if self.max is None:
            return TranslatableText(
                f'Exercise must require grouping by at least {self.min} columns',
                it=f'L\'esercizio deve richiedere raggruppamento per almeno {self.min} colonne'
            )
        if self.min == self.max:
            return TranslatableText(
                f'Exercise must require grouping by exactly {self.min} columns',
                it=f'L\'esercizio deve richiedere raggruppamento per esattamente {self.min} colonne'
            )
        return TranslatableText(
            f'Exercise must require grouping by between {self.min} and {self.max} columns',
            it=f'L\'esercizio deve richiedere raggruppamento tra {self.min} e {self.max} colonne'
        )

