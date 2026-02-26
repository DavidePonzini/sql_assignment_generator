from .base import QueryConstraint
from sqlscope import Query
from ...exceptions import ConstraintValidationError
from ...translatable_text import TranslatableText

class SelectedColumns(QueryConstraint):
    '''Requires a specific number of columns in the main SELECT clause.'''

    def __init__(self, min_: int = 1, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_

    def validate(self, query: Query) -> None:
        output = query.main_query.output

        columns = len(output.columns)

        if self.max is None:
            if columns < self.min:
                raise ConstraintValidationError(
                    TranslatableText(
                        f'Query must select at least {self.min} columns, but selected {columns} columns.',
                        it=f'La query deve selezionare almeno {self.min} colonne, ma ne ha selezionate {columns}.'
                    )
                )
            return
        if not (self.min <= columns <= self.max):
            raise ConstraintValidationError(
                TranslatableText(
                    f'Query must select between {self.min} and {self.max} columns, but selected {columns} columns.',
                    it=f'La query deve selezionare tra {self.min} e {self.max} colonne, ma ne ha selezionate {columns}.'
                )
            )

    @property
    def description(self) -> TranslatableText:
        if self.max is None:
            return TranslatableText(
                f'Query must select at least {self.min} columns',
                it=f'La query deve selezionare almeno {self.min} colonne'
            )
        if self.min == self.max:
            return TranslatableText(
                f'Query must select exactly {self.min} columns',
                it=f'La query deve selezionare esattamente {self.min} colonne'
            )
        return TranslatableText(
            f'Query must select between {self.min} and {self.max} columns',
            it=f'La query deve selezionare tra {self.min} e {self.max} colonne'
        )

class NoAlias(QueryConstraint):
    '''
    Requires that no columns in the SELECT clause are renamed (no aliases for columns).
    '''

    def validate(self, query: Query) -> None:
        output = query.main_query.output

        for col in output.columns:
            if col.name != col.real_name:
                raise ConstraintValidationError(
                    TranslatableText(
                        'Columns in SELECT must not be renamed (must not use aliases).',
                        it='Le colonne nella SELECT non devono essere rinominate (non devono usare alias).'
                    )
                )

    @property
    def description(self) -> TranslatableText:
        return TranslatableText(
            'Columns in SELECT must not be renamed (must not use aliases).',
            it='Le colonne nella SELECT non devono essere rinominate (non devono usare alias).'
        )

class Alias(QueryConstraint):
    '''
        Requires a number of columns in the SELECT clause to be renamed using an alias (AS).
    '''

    def __init__(self, min_: int, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_


    def validate(self, query: Query) -> None:
        output = query.main_query.output

        alias_count = 0
        for col in output.columns:
            if col.name != col.real_name:
                alias_count += 1

        if self.max is None:
            if alias_count < self.min:
                raise ConstraintValidationError(
                    TranslatableText(
                        f'At least {self.min} columns in SELECT must be renamed using an alias (AS), but only {alias_count} were found.',
                        it=f'Almeno {self.min} colonne nella SELECT devono essere rinominate usando un alias (AS), ma ne sono state trovate solo {alias_count}.'
                    )
                )
            return
        
        if not (self.min <= alias_count <= self.max):
            raise ConstraintValidationError(
                TranslatableText(
                    f'Between {self.min} and {self.max} columns in SELECT must be renamed using an alias (AS), but {alias_count} were found.',
                    it=f'Tra {self.min} e {self.max} colonne nella SELECT devono essere rinominate usando un alias (AS), ma ne sono state trovate {alias_count}.'
                )
            )

    @property
    def description(self) -> TranslatableText:
        if self.max is None:
            return TranslatableText(
                f'At least {self.min} columns in SELECT must be renamed using an alias (AS)',
                it=f'Almeno {self.min} colonne nella SELECT devono essere rinominate usando un alias (AS)'
            )
        if self.min == self.max:
            return TranslatableText(
                f'Exactly {self.min} columns in SELECT must be renamed using an alias (AS)',
                it=f'Esattamente {self.min} colonne nella SELECT devono essere rinominate usando un alias (AS)'
            )
        return TranslatableText(
            f'Between {self.min} and {self.max} columns in SELECT must be renamed using an alias (AS)',
            it=f'Tra {self.min} e {self.max} colonne nella SELECT devono essere rinominate usando un alias (AS)'
        )