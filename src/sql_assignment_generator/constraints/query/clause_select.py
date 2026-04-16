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

        aliased_columns: list[tuple[str, str]] = []  # List of (real_name, alias) for aliased columns
        unaliased_columns: list[tuple[str, str]] = []  # List of (real_name, alias) for aliased columns
        for col in output.columns:
            if col.table_idx is None:
                # computed column, skip it
                continue

            if col.name != col.real_name:
                aliased_columns.append((col.real_name, col.name))
            else:
                unaliased_columns.append((col.name, col.name))

        if self.max is None:
            if len(aliased_columns) < self.min:
                raise ConstraintValidationError(
                    TranslatableText(
                        f'At least {self.min} non-aggregate columns in SELECT must be renamed using an alias (AS), but only {len(aliased_columns)} were found. Rename the remaining columns (currently not aliased: {", ".join([name for name, _ in unaliased_columns])}) to meet the requirement.\n{query.sql}',
                        it=f'Almeno {self.min} colonne nella SELECT devono essere rinominate usando un alias (AS), ma ne sono state trovate solo {len(aliased_columns)}. Rinomina le colonne rimanenti (attualmente non aliasate: {", ".join([name for name, _ in unaliased_columns])}).',
                    )
                )
            return
        
        if not (self.min <= len(aliased_columns) <= self.max):
            raise ConstraintValidationError(
                TranslatableText(
                    f'Between {self.min} and {self.max} non-aggregate columns in SELECT must be renamed using an alias (AS), but {len(aliased_columns)} were found. Rename the columns to meet the requirement (currently not aliased: {", ".join([name for name, _ in unaliased_columns])}).',
                    it=f'Tra {self.min} e {self.max} colonne nella SELECT devono essere rinominate usando un alias (AS), ma ne sono state trovate {len(aliased_columns)}. Rinomina le colonne per soddisfare il requisito (attualmente non aliasate: {", ".join([name for name, _ in unaliased_columns])}).',
                )
            )

    @property
    def description(self) -> TranslatableText:
        if self.max is None:
            return TranslatableText(
                f'At least {self.min} non-aggregate columns in SELECT must be renamed using an alias (AS)',
                it=f'Almeno {self.min} colonne nella SELECT devono essere rinominate usando un alias (AS)'
            )
        if self.min == self.max:
            return TranslatableText(
                f'Exactly {self.min} non-aggregate columns in SELECT must be renamed using an alias (AS)',
                it=f'Esattamente {self.min} colonne nella SELECT devono essere rinominate usando un alias (AS)'
            )
        return TranslatableText(
            f'Between {self.min} and {self.max} non-aggregate columns in SELECT must be renamed using an alias (AS)',
            it=f'Tra {self.min} e {self.max} colonne nella SELECT devono essere rinominate usando un alias (AS)'
        )
    
class OriginalName(QueryConstraint):
    '''
    Requires that at least n columns in the SELECT clause are not renamed (i.e. they keep their original name).
    '''

    def __init__(self, min_: int, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_

    def validate(self, query: Query) -> None:
        output = query.main_query.output

        original_name_columns = [col for col in output.columns if col.name == col.real_name and col.table_idx is not None]

        if self.max is None:
            if len(original_name_columns) < self.min:
                raise ConstraintValidationError(
                    TranslatableText(
                        f'At least {self.min} non-aggregate columns in SELECT must keep their original name (i.e. not be renamed using an alias), but only {len(original_name_columns)} were found. Add another {self.min - len(original_name_columns)} column(s) that keep their original name to meet the requirement',
                        it=f'Almeno {self.min} colonne nella SELECT devono mantenere il loro nome originale (cioè non essere rinominate usando un alias), ma ne sono state trovate solo {len(original_name_columns)}. Aggiungi altre {self.min - len(original_name_columns)} colonna(e) che mantengano il loro nome originale per soddisfare il requisito.',
                    )
                )
            return
        
        if not (self.min <= len(original_name_columns) <= self.max):
            raise ConstraintValidationError(
                TranslatableText(
                    f'Between {self.min} and {self.max} non-aggregate columns in SELECT must keep their original name (i.e. not be renamed using an alias), but {len(original_name_columns)} were found. Adjust the columns to meet the requirement (currently {len(original_name_columns)} columns keep their original name).',
                    it=f'Tra {self.min} e {self.max} colonne nella SELECT devono mantenere il loro nome originale (cioè non essere rinominate usando un alias), ma ne sono state trovate {len(original_name_columns)}. Regola le colonne per soddisfare il requisito (attualmente {len(original_name_columns)} colonne mantengono il loro nome originale).',
                )
            )
        
    @property
    def description(self) -> TranslatableText:
        if self.max is None:
            return TranslatableText(
                f'At least {self.min} non-aggregate columns in SELECT must keep their original name (i.e. not be renamed using an alias)',
                it=f'Almeno {self.min} colonne nella SELECT devono mantenere il loro nome originale (cioè non essere rinominate usando un alias)'
            )
        if self.min == self.max:
            return TranslatableText(
                f'Exactly {self.min} non-aggregate columns in SELECT must keep their original name (i.e. not be renamed using an alias)',
                it=f'Esattamente {self.min} colonne nella SELECT devono mantenere il loro nome originale (cioè non essere rinominate usando un alias)'
            )
        return TranslatableText(
            f'Between {self.min} and {self.max} non-aggregate columns in SELECT must keep their original name (i.e. not be renamed using an alias)',
            it=f'Tra {self.min} e {self.max} colonne nella SELECT devono mantenere il loro nome originale (cioè non essere rinominate usando un alias)'
        )