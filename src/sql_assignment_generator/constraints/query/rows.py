from sql_assignment_generator.constraints.schema import tables

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

        all_tables_names = query.catalog[query.search_path].table_names
        all_tables = [query.catalog[query.search_path][table_name] for table_name in all_tables_names]
        all_constraints = [(t.name, c) for t in all_tables for c in t.unique_constraints]
        columns_to_avoid: set[tuple[str, ...]] = set()

        for table_name, constraint in all_constraints:
            cols: list[str] = []
            for column in constraint.columns:
                cols.append(f'{table_name}.{column.name}')
            columns_to_avoid.add(tuple(cols))

        if not has_distinct_constraint:
            raise ConstraintValidationError(
                TranslatableText(
                    f'The exercise must use the DISTINCT keyword to eliminate duplicate rows that would otherwise be returned, but the query does not use DISTINCT in the main SELECT statement. '\
                        f'You can achieve this by selecting columns that do not form a unique key and that do not have unique constraints on the referenced tables. '\
                        f'Current unique constraints on output columns: {output_constraints}. '\
                        f'Don\'t select the following combinations of columns: {columns_to_avoid}, since they have unique constraints, unless you only select a part of them (i.e. (a, b) -> you can select `a` or `b`, but not both).',

                    it=f'L\'esercizio deve usare la parola chiave DISTINCT per eliminare le righe duplicate che altrimenti verrebbero restituite, ma la query non usa DISTINCT nella dichiarazione SELECT principale. '\
                        f'Puoi ottenere questo risultato selezionando colonne che non formano una chiave univoca e che non hanno vincoli univoci sulle tabelle referenziate. '\
                        f'Vincoli univoci correnti sulle colonne di output: {output_constraints}. '\
                        f'Non selezionare le seguenti combinazioni di colonne: {columns_to_avoid}, poiché hanno vincoli univoci, a meno che tu non selezioni solo una parte di esse (es. (a, b) -> puoi selezionare `a` o `b`, ma non entrambi).'
                )
            )
        if len(other_constraints) > 0:
            raise ConstraintValidationError(
                TranslatableText(
                    f'The exercise must use the DISTINCT keyword to eliminate duplicate rows that would otherwise be returned, but the query has other unique constraints on the output columns. '\
                        f'You can achieve this by selecting columns that do not form a unique key and that do not have unique constraints on the referenced tables. '\
                        f'Current unique constraints: {output_constraints} (only DISTINCT should be present) ' \
                        f'Don\'t select the following combinations of columns: {columns_to_avoid}, since they have unique constraints, unless you only select a part of them (i.e. (a, b) -> you can select `a` or `b`, but not both).',

                    it=f'L\'esercizio deve usare la parola chiave DISTINCT per eliminare le righe duplicate che altrimenti verrebbero restituite, ma la query ha altri vincoli univoci sulle colonne di output. '\
                        f'Puoi ottenere questo risultato selezionando colonne che non formano una chiave univoca e che non hanno vincoli univoci sulle tabelle referenziate. '\
                        f'Vincoli univoci correnti: {output_constraints} (solo DISTINCT dovrebbe essere presente) ' \
                        f'Non selezionare le seguenti combinazioni di colonne: {columns_to_avoid}, poiché hanno vincoli univoci, a meno che tu non selezioni solo una parte di esse (es. (a, b) -> puoi selezionare `a` o `b`, ma non entrambi).'
                )
            )

    @property
    def description(self) -> TranslatableText:
        return TranslatableText(
            'The exercise must use the DISTINCT keyword to eliminate duplicate rows that would otherwise be returned,',
            it='L\'esercizio deve usare la parola chiave DISTINCT per eliminare le righe duplicate che altrimenti verrebbero restituite,'
        )
