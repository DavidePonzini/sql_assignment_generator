from collections import Counter
from .base import SchemaConstraint
from sqlglot import exp 
from ...exceptions import ConstraintMergeError, ConstraintValidationError
from sqlscope import Catalog
from ...translatable_text import TranslatableText

class MinRows(SchemaConstraint):
    '''Requires that EACH table found in the insert list has a specific minimum number of rows inserted.'''

    def __init__(self, min_: int = 3) -> None:
        self.min = min_

    def validate(self, catalog: Catalog, tables_sql: list[exp.Create], values_sql: list[exp.Insert]) -> None:
        table_row_counts = Counter()

        for value in values_sql:

            table_name = value.this.this.name.lower()
            values_node = value.expression

            # verify the format INSERT INTO ... VALUES ...
            if isinstance(values_node, exp.Values):     # list of insert row: (val1), (val2)...
                rows_in_statement = len(values_node.expressions)
                table_row_counts[table_name] += rows_in_statement

        # if no tables found but min > 0, fail
        if not table_row_counts and self.min > 0:
            raise ConstraintValidationError(
                TranslatableText(
                    f'No rows found for any table, which is less than the required minimum of {self.min} rows per table.',
                    it=f'Nessuna riga trovata per nessuna tabella, che è meno del minimo richiesto di {self.min} righe per tabella.'
                )
            )

        # check each table meets minimum row requirement
        for table_name, count in table_row_counts.items():
            if count < self.min:
                raise ConstraintValidationError(
                    TranslatableText(
                        f'Table "{table_name}" has {count} rows, which is less than the required minimum of {self.min} rows.',
                        it=f'La tabella "{table_name}" ha {count} righe, che è meno del minimo richiesto di {self.min} righe.'
                    )
                )

    @property
    def description(self) -> TranslatableText:
        return TranslatableText(
            f'Dataset must have at least {self.min} rows of data for each table.',
            it=f'Il dataset deve avere almeno {self.min} righe di dati per ogni tabella.'
        )
    
    def merge(self, other: SchemaConstraint) -> 'MinRows':
        if not isinstance(other, MinRows):
            raise ConstraintMergeError(self, other)

        min_rows = max(self.min, other.min)
        return MinRows(min_=min_rows)

class SingleInsertPerTable(SchemaConstraint):
    '''Requires that each table has exactly one INSERT statement (multi-row format).'''

    def validate(self, catalog: Catalog, tables_sql: list[exp.Create], values_sql: list[exp.Insert]) -> None:
        table_insert_counts = Counter()

        for value in values_sql:
            table_name = value.this.this.name.lower()
            table_insert_counts[table_name] += 1

        violating_tables = [t for t, c in table_insert_counts.items() if c > 1]
        if violating_tables:
            table_list = ', '.join(f'"{t}"' for t in violating_tables)
            raise ConstraintValidationError(
                TranslatableText(
                    f'Tables {table_list} have multiple INSERT statements. Each table must have exactly one multi-row INSERT.',
                    it=f'Le tabelle {table_list} hanno più istruzioni INSERT. Ogni tabella deve avere esattamente un\'istruzione INSERT multi-riga.'
                )
            )

    @property
    def description(self) -> TranslatableText:
        return TranslatableText(
            'Each table must have exactly one INSERT INTO statement with all rows in multi-row format.',
            it='Ogni tabella deve avere esattamente un\'istruzione INSERT INTO con tutte le righe in formato multi-riga.'
        )

    def merge(self, other: SchemaConstraint) -> 'SingleInsertPerTable':
        if not isinstance(other, SingleInsertPerTable):
            raise ConstraintMergeError(self, other)
        return SingleInsertPerTable()