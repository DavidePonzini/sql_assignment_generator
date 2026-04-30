from .base import SchemaConstraint
from sqlglot import exp
from sqlscope import Catalog
from sqlscope.catalog.constraint import ConstraintType
from ...exceptions import ConstraintMergeError, ConstraintValidationError
from collections import Counter
from ...translatable_text import TranslatableText

class MinTables(SchemaConstraint):
    '''Requires the schema to have a specific number of tables.'''

    def __init__(self, min_tables: int = 5) -> None:
        self.min_tables = min_tables

    def validate(self, catalog: Catalog, tables_sql: list[exp.Create], values_sql: list[exp.Insert]) -> None:
        table_count = len(tables_sql)

        if table_count < self.min_tables:
            raise ConstraintValidationError(
                TranslatableText(
                    f'Schema has {table_count} tables, which is less than the required minimum of {self.min_tables} tables. Add more CREATE TABLE statements to your dataset SQL.',
                    it=f'Lo schema ha {table_count} tabelle, che è meno del minimo richiesto di {self.min_tables} tabelle. Aggiungi più statement CREATE TABLE al tuo dataset SQL.'
                )
            )

    @property
    def description(self) -> TranslatableText:
        return TranslatableText(
            f'Schema must be comprised of at least {self.min_tables} tables',
            it=f'Lo schema deve essere composto da almeno {self.min_tables} tabelle'
        )
    
    def merge(self, other: SchemaConstraint) -> 'MinTables':
        if not isinstance(other, MinTables):
            raise ConstraintMergeError(self, other)
        
        return MinTables(min_tables=max(self.min_tables, other.min_tables))
    
class MinChecks(SchemaConstraint):
    '''Requires the schema to have a specific number of CHECK constraints.'''

    def __init__(self, min_: int = 1, max_: int | None = None) -> None:
        self.min = min_
        self.max = max_

    def validate(self, catalog: Catalog, tables_sql: list[exp.Create], values_sql: list[exp.Insert]) -> None:
        total_checks = 0
        
        for table in tables_sql:
            checks_found = list(table.find_all(exp.Check, exp.CheckColumnConstraint))
            total_checks += len(checks_found)

        if self.max is None:
            if total_checks < self.min:
                raise ConstraintValidationError(
                    TranslatableText(
                        f'Schema has {total_checks} CHECK constraints, which is less than the required minimum of {self.min}. Add more CHECK constraints to your CREATE TABLE statements in the dataset SQL.',
                        it=f'Lo schema ha {total_checks} constraint CHECK, che è meno del minimo richiesto di {self.min}. Aggiungi più constraint CHECK ai tuoi statement CREATE TABLE nel dataset SQL.'
                    )
                )
        else:
            if not (self.min <= total_checks <= self.max):
                raise ConstraintValidationError(
                    TranslatableText(
                        f'Schema has {total_checks} CHECK constraints, which is not within the required range of {self.min} to {self.max}.',
                        it=f'Lo schema ha {total_checks} constraint CHECK, che non è compreso nell\'intervallo richiesto di {self.min} a {self.max}.'
                    )
                )
        
    @property
    def description(self) -> TranslatableText:
        if self.max is None: 
            return TranslatableText(
                f'Schema must have minimum {self.min} CHECK constraints',
                it=f'Lo schema deve avere almeno {self.min} constraint CHECK'
            )
        elif self.min == self.max: 
            return TranslatableText(
                f'Schema must have exactly {self.min} CHECK constraints',
                it=f'Lo schema deve avere esattamente {self.min} constraint CHECK'
            )
        else: 
            return TranslatableText(
                f'Schema must have between {self.min} and {self.max} CHECK constraints',
                it=f'Lo schema deve avere tra {self.min} e {self.max} constraint CHECK'
            )
        
    def merge(self, other: SchemaConstraint) -> 'MinChecks':
        if not isinstance(other, MinChecks):
            raise ConstraintMergeError(self, other)
        
        merged_min = max(self.min, other.min)

        if self.max is None:
            merged_max = other.max
        elif other.max is None:
            merged_max = self.max
        else:
            merged_max = min(self.max, other.max)
        
        return MinChecks(min_=merged_min, max_=merged_max)
    
class MinColumns(SchemaConstraint):
    '''Requires that at least a specific number of tables in the schema have at least a specific number of columns.'''

    def __init__(self, columns: int = 2, tables: int = 1) -> None:
        self.columns = columns
        self.tables = tables

    def validate(self, catalog: Catalog, tables_sql: list[exp.Create], values_sql: list[exp.Insert]) -> None:
        valid_tables_count = 0

        for schema_name in catalog.schema_names:
            for table_name in catalog[schema_name].table_names:
                table = catalog[schema_name][table_name]
                
                # count columns in the table
                column_count = len(table.columns)
                
                # if column count meets the minimum, increment valid table count
                if column_count >= self.columns:
                    valid_tables_count += 1
        
        if valid_tables_count < self.tables:
            raise ConstraintValidationError(
                TranslatableText(
                    f'Schema has {valid_tables_count} tables with at least {self.columns} columns, which is less than the required minimum of {self.tables} tables. Add more columns to the existing tables or add new tables with the required number of columns.',
                    it=f'Lo schema ha {valid_tables_count} tabelle con almeno {self.columns} colonne, che è meno del minimo richiesto di {self.tables} tabelle. Aggiungi più colonne alle tabelle esistenti o aggiungi nuove tabelle con il numero richiesto di colonne.'
                )
            )

    @property
    def description(self) -> TranslatableText:
        return TranslatableText(
            f'Schema must have at least {self.tables} tables with at least {self.columns} columns',
            it=f'Lo schema deve avere almeno {self.tables} tabelle con almeno {self.columns} colonne'
        )

    def merge(self, other: SchemaConstraint) -> 'MinColumns':
        if not isinstance(other, MinColumns):
            raise ConstraintMergeError(self, other)
        
        # Merging by taking the maximum of min_tables and min_columns
        merged_min_tables = max(self.tables, other.tables)
        merged_min_columns = max(self.columns, other.columns)

        return MinColumns(
            tables=merged_min_tables,
            columns=merged_min_columns,
        )
    
class ComplexColumnName(SchemaConstraint):
    '''
    Requires the schema to contain a specific minimum number of columns
    whose names contain at least 15 characters
    and at least one underscore separator ('_').
    '''

    def __init__(self, min_columns: int = 1) -> None:
        self.min_columns = min_columns

    def validate(self, catalog: Catalog, tables_sql: list[exp.Create], values_sql: list[exp.Insert]) -> None:
        complex_cols_found = []

        for schema_name in catalog.schema_names:
            for table_name in catalog[schema_name].table_names:
                table = catalog[schema_name][table_name]
                
                for column in table.columns:
                    col_name = column.real_name
                    
                    # check criteria
                    if len(col_name) >= 15 and '_' in col_name:
                        complex_cols_found.append(col_name)

        if len(complex_cols_found) < self.min_columns:
            raise ConstraintValidationError(
                TranslatableText(
                    f'Schema has {len(complex_cols_found)} columns with complex names ({complex_cols_found}), which is less than the required minimum of {self.min_columns}. Add more columns with names that are at least 15 characters long and contain an underscore ("_") to your CREATE TABLE statements in the dataset SQL.',
                    it=f'Lo schema ha {len(complex_cols_found)} colonne con nomi complessi ({complex_cols_found}), che è meno del minimo richiesto di {self.min_columns}. Aggiungi più colonne con nomi che siano almeno di 15 caratteri e contengano un underscore ("_") ai tuoi statement CREATE TABLE nel dataset SQL.'
                )
            )
    
    @property
    def description(self) -> TranslatableText:
        return TranslatableText(
            f'Schema must have at least {self.min_columns} columns with complex and lengthy names (length >= 15 and containing "_")',
            it=f'Lo schema deve avere almeno {self.min_columns} colonne con nomi complessi e lunghi (lunghezza >= 15 e contenente "_")'
        )

    def merge(self, other: SchemaConstraint) -> 'ComplexColumnName':
        if not isinstance(other, ComplexColumnName):
            raise ConstraintMergeError(self, other)
        
        min_cols = max(self.min_columns, other.min_columns)
        return ComplexColumnName(min_columns=min_cols)
    

class SameColumnNames(SchemaConstraint):
    '''
    Requires that a specific number of tables have at least 2 non-key (PK/FK) columns with the same names.
    '''

    def __init__(self, pairs: int = 1) -> None:
        self.pairs = pairs

    def validate(self, catalog: Catalog, tables_sql: list[exp.Create], values_sql: list[exp.Insert]) -> None:
        name_counts: Counter[str] = Counter()
        '''Counter for column names across all tables.'''

        for schema_name in catalog.schema_names:
            for table_name in catalog[schema_name].table_names:
                table = catalog[schema_name][table_name]

                pk_constraints = [c for c in table.unique_constraints if c.constraint_type == ConstraintType.PRIMARY_KEY]
                pk_cols: set[str] = set()
                '''Set of column names that are part of primary keys for the current table.'''
                
                for pk in pk_constraints:
                    for col in pk.columns:
                        pk_cols.add(col.name)

                for column in table.columns:
                    col_name = column.real_name
                    if col_name in pk_cols or column.is_fk:
                        continue

                    name_counts[col_name] += 1

        tables_with_same_col_names = sum(1 for count in name_counts.values() if count >= 2)
        if tables_with_same_col_names < self.pairs:
            raise ConstraintValidationError(
                TranslatableText(
                    f'Schema has {tables_with_same_col_names} pair(s) of non-key columns with the same name, '
                    f'which is less than the required minimum of {self.pairs} pair(s).'
                    f'Current column name counts: {name_counts}. Columns not counted are part of PKs/FKs.'
                    f'Add more columns without key constraints that share the same names across different tables to meet the requirement.',
                    it=f'Lo schema ha {tables_with_same_col_names} coppia/e di colonne non chiave con lo stesso nome, '
                    f'che è meno del minimo richiesto di {self.pairs} coppia/e.'
                    f'Conteggio corrente dei nomi delle colonne: {name_counts}. Le colonne non conteggiate fanno parte di PK/FK.'
                    f'Aggiungi più colonne senza vincoli di chiave con gli stessi nomi in tabelle diverse per soddisfare il requisito.'
                )
            )
    
    @property
    def description(self) -> TranslatableText:
        return TranslatableText(
            f'In CREATE TABLE must have at least {self.pairs} pair(s) of non-key columns (either PKs or FKs) with the same name but different semantic meaning',
            it=f'Nel CREATE TABLE deve avere almeno {self.pairs} coppia/e di colonne non chiave (PK o FK) con lo stesso nome ma significato semantico diverso'
        )

    def merge(self, other: SchemaConstraint) -> 'SameColumnNames':
        if not isinstance(other, SameColumnNames):
            raise ConstraintMergeError(self, other)
        
        min_tables = max(self.pairs, other.pairs)
        return SameColumnNames(pairs=min_tables)
    
class MaxColumns(SchemaConstraint):
    '''Requires the schema to have a specific maximum number of columns for each table.'''

    def __init__(self, max_columns: int) -> None:
        self.max_columns = max_columns

    def validate(self, catalog: Catalog, tables_sql: list[exp.Create], values_sql: list[exp.Insert]) -> None:
        for schema_name in catalog.schema_names:
            for table_name in catalog[schema_name].table_names:
                table = catalog[schema_name][table_name]
                column_count = len(table.columns)

                if column_count > self.max_columns:
                    raise ConstraintValidationError(
                        TranslatableText(
                            f'Table "{table_name}" has {column_count} columns, which exceeds the maximum allowed of {self.max_columns}. Reduce the number of columns in this table to meet the requirement.',
                            it=f'La tabella "{table_name}" ha {column_count} colonne, che supera il massimo consentito di {self.max_columns}. Riduci il numero di colonne in questa tabella per soddisfare il requisito.'
                        )
                    )
                
    @property
    def description(self) -> TranslatableText:
        return TranslatableText(
            f'Each table in the schema must have at most {self.max_columns} columns',
            it=f'Ogni tabella nello schema deve avere al massimo {self.max_columns} colonne'
        )
    
    def merge(self, other: SchemaConstraint) -> 'MaxColumns':
        if not isinstance(other, MaxColumns):
            raise ConstraintMergeError(self, other)
        
        max_cols = min(self.max_columns, other.max_columns)
        return MaxColumns(max_columns=max_cols)