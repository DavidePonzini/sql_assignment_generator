from .base import QueryConstraint
from sqlscope import Query
from sqlscope.catalog.constraint import ConstraintType
from ...exceptions import ConstraintValidationError
from ...translatable_text import TranslatableText

class Duplicates(QueryConstraint):
    '''
    Require the query to return duplicate rows
    '''

    def validate(self, query: Query) -> None:
        main_query = query.main_query

        output = main_query.output
        output_constraints = output.unique_constraints

        if len(output_constraints) > 0:
            raise ConstraintValidationError(
                TranslatableText(
                    f'The exercise must return duplicate rows, but the query has unique constraints on the output columns. Current unique constraints: {output_constraints}',
                    it=f'L\'esercizio deve restituire righe duplicate, ma la query ha vincoli univoci sulle colonne di output. Vincoli univoci correnti: {output_constraints}'
                )
            )
    
    @property
    def description(self) -> TranslatableText:
        return TranslatableText(
            'The exercise must return duplicate rows, i.e., no unique/primary key on any columns in the SELECT clause, no DISTINCT keyword, and no grouping.',
            it='L\'esercizio deve restituire righe duplicate, ovvero nessuna chiave univoca/primaria su alcune colonne nella clausola SELECT, nessuna parola chiave DISTINCT e nessun raggruppamento.'
        )

class NoDuplicates(QueryConstraint):
    '''
    Require the query to return unique rows, even if DISTINCT is not used
    '''

    def validate(self, query: Query) -> None:
        main_query = query.main_query

        output_constraints = main_query.output.unique_constraints

        other_constraints = [c for c in output_constraints if c.constraint_type != ConstraintType.DISTINCT]

        if len(other_constraints) == 0:
            raise ConstraintValidationError(
                TranslatableText(
                    'The exercise must return unique rows, but the query has no unique constraints on the output columns (e.g. DISTINCT, GROUP BY, or selection of a primary key).',
                    it='L\'esercizio deve restituire righe uniche, ma la query non ha vincoli univoci sulle colonne di output (es. DISTINCT, GROUP BY o selezione di una chiave primaria).'
                )
            )
    
    @property
    def description(self) -> TranslatableText:
        return TranslatableText(
            'The exercise must return unique rows, i.e., at least one unique constraint on the output columns (e.g. DISTINCT, GROUP BY, or selection of a primary key).',
            it='L\'esercizio deve restituire righe uniche, ovvero almeno un vincolo univoco sulle colonne di output (es. DISTINCT, GROUP BY o selezione di una chiave primaria).'
        )

class Distinct(QueryConstraint):
    '''
    Require the query to use the DISTINCT keyword to eliminate duplicate rows.
    This means that the query must return duplicate rows without DISTINCT, and return unique rows with DISTINCT.
    '''

    def validate(self, query: Query) -> None:
        main_query = query.main_query

        output_constraints = main_query.output.unique_constraints

        has_distinct_constraint = any(c.constraint_type == ConstraintType.DISTINCT for c in output_constraints)
        other_constraints = [c for c in output_constraints if c.constraint_type != ConstraintType.DISTINCT]

        if not has_distinct_constraint or len(other_constraints) > 0:
            raise ConstraintValidationError(
                TranslatableText(
                    'The exercise must use the DISTINCT keyword to eliminate duplicate rows, but the query does not use DISTINCT. Without DISTINCT, the query would return duplicate rows, but with DISTINCT it returns unique rows.',
                    it='L\'esercizio deve usare la parola chiave DISTINCT per eliminare le righe duplicate, ma la query non la usa. Senza DISTINCT, la query restituirebbe righe duplicate, ma con DISTINCT restituisce righe uniche.'
                )
            )

    @property
    def description(self) -> TranslatableText:
        return TranslatableText(
            'The exercise must use the DISTINCT keyword to eliminate duplicate rows, ' \
            'meaning that, had DISTINCT not been used, the query would have returned duplicate rows.',
            it='L\'esercizio deve usare la parola chiave DISTINCT per eliminare le righe duplicate, ' \
               'significando che, se non fosse stata usata DISTINCT, la query avrebbe restituito righe duplicate.'
        )
