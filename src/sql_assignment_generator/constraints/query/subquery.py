from collections import Counter
from .base import QueryConstraint
from sqlscope import Query
from ...exceptions import ConstraintValidationError
from ...translatable_text import TranslatableText

class NoSubquery(QueryConstraint):
    '''Requires the absence of subqueries in the SQL query.'''

    def validate(self, query: Query) -> None:

        for select in query.selects:
            if len(select.subqueries) > 0:
                raise ConstraintValidationError(
                    TranslatableText(
                        'Exercise must not require any subqueries, but at least one subquery was found in the query.',
                        it='L\'esercizio non deve richiedere alcuna subquery, ma è stata trovata almeno una subquery nella query.'
                    )
                )
    @property
    def description(self) -> TranslatableText:
        return TranslatableText(
            'Exercise must not require any subqueries.',
            it='L\'esercizio non deve richiedere alcuna subquery.'
        )
    
class NoNesting(QueryConstraint):
    '''Requires the absence of nested subqueries in the SQL query.'''
    def validate(self, query: Query) -> None:
        for select in query.selects:
            for subquery, sql, depth in select.subqueries:
                if depth >= 2:
                    raise ConstraintValidationError(
                        TranslatableText(
                            'Exercise must not require any nested subqueries, but at least one nested subquery was found in the query.',
                            it='L\'esercizio non deve richiedere alcuna subquery annidata, ma è stata trovata almeno una subquery annidata nella query.'
                        )
                    )

    @property
    def description(self) -> TranslatableText:
        return TranslatableText(
            'Exercise must not require any nested subqueries.',
            it='L\'esercizio non deve richiedere alcuna subquery annidata.'
        )

class Subqueries(QueryConstraint):
    '''
    Requires the presence of a certain number of unnested subqueries in the SQL query.
    Unnested subqueries are subqueries that are not nested inside another subquery.
    They can contain nested subqueries within them, but at least `min_` of them must be at the same level.
    '''
    def __init__(self, min_: int = 1, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_

    def validate(self, query: Query) -> None:
        unnested_subquery_counts: list[int] = []
        
        for select in query.selects:
            select = select.strip_subqueries(min_depth=2) # Strip all nested subqueries, leaving only unnested subqueries at the top level of the SELECT clause
            unnested_subquery_counts.append(len(select.subqueries))

        for count in unnested_subquery_counts:
            if self.max is None:
                if count >= self.min:
                    return
                continue
            if self.min <= count <= self.max:
                return
            continue

        if self.max is None:
            raise ConstraintValidationError(
                TranslatableText(
                    f'Exercise must require at least {self.min} unnested subqueries, but no SELECT clause has that many unnested subqueries.',
                    it=f'L\'esercizio deve richiedere almeno {self.min} sottoscrizioni non annidate, ma nessuna clausola SELECT ha quel numero di sottoscrizioni non annidate.'
                )
            )
        raise ConstraintValidationError(
            TranslatableText(
                f'Exercise must require between {self.min} and {self.max} unnested subqueries, but no SELECT clause has that many unnested subqueries.',
                it=f'L\'esercizio deve richiedere tra {self.min} e {self.max} sottoscrizioni non annidate, ma nessuna clausola SELECT ha quel numero di sottoscrizioni non annidate.'
            )
        )

    @property
    def description(self) -> TranslatableText:
        if self.max is None:
            return TranslatableText(
                f'Exercise must require at least {self.min} unnested subqueries.',
                it=f'L\'esercizio deve richiedere almeno {self.min} sottoscrizioni non annidate.'
            )
        if self.min == self.max:
            return TranslatableText(
                f'Exercise must require exactly {self.min} unnested subqueries.',
                it=f'L\'esercizio deve richiedere esattamente {self.min} sottoscrizioni non annidate.'
            )
        return TranslatableText(
            f'Exercise must require between {self.min} and {self.max} unnested subqueries.',
            it=f'L\'esercizio deve richiedere tra {self.min} e {self.max} sottoscrizioni non annidate.'
        )
class NestedSubqueries(QueryConstraint):
    '''Requires the presence of a certain number of subqueries that contain at least one nested subquery.'''

    def __init__(self, min_: int = 1, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_

    def validate(self, query: Query) -> None:
        nested_counts = Counter()
        
        for select in query.selects:
            for subquery, sql, depth in select.subqueries:
                if depth >= 2: # Only consider subqueries that are nested at least 2 levels deep (i.e. subqueries that contain at least one nested subquery)
                    nested_counts[select] += 1

        max_nested = max(nested_counts.values(), default=0)

        if self.max is None:
            if max_nested >= self.min:
                return
            raise ConstraintValidationError(
                TranslatableText(
                    f'Exercise must require at least {self.min} subqueries containing nested subqueries, but no SELECT clause has that many nested subqueries. Current nesting counts: {nested_counts}',
                    it=f'L\'esercizio deve richiedere almeno {self.min} sottoscrizioni contenenti sottoscrizioni annidate, ma nessuna clausola SELECT ha quel numero di sottoscrizioni annidate. Conteggio corrente: {nested_counts}'
                )
            )
        if self.min <= max_nested <= self.max:
            return
        raise ConstraintValidationError(
            TranslatableText(
                f'Exercise must require between {self.min} and {self.max} subqueries containing nested subqueries, but no SELECT clause has that many nested subqueries. Current nesting counts: {nested_counts}',
                it=f'L\'esercizio deve richiedere tra {self.min} e {self.max} sottoscrizioni contenenti sottoscrizioni annidate, ma nessuna clausola SELECT ha quel numero di sottoscrizioni annidate. Conteggio corrente: {nested_counts}'
            )
        )

    @property
    def description(self) -> TranslatableText:
        if self.max is None:
            return TranslatableText(
                f'Exercise must require at least {self.min} subqueries containing nested subqueries.',
                it=f'L\'esercizio deve richiedere almeno {self.min} sottoscrizioni contenenti sottoscrizioni annidate.'
            )
        if self.min == self.max:
            return TranslatableText(
                f'Exercise must require exactly {self.min} subqueries containing nested subqueries.',
                it=f'L\'esercizio deve richiedere esattamente {self.min} sottoscrizioni contenenti sottoscrizioni annidate.'
            )
        return TranslatableText(
            f'Exercise must require between {self.min} and {self.max} subqueries containing nested subqueries.',
            it=f'L\'esercizio deve richiedere tra {self.min} e {self.max} sottoscrizioni contenenti sottoscrizioni annidate.'
        )