from .base import SchemaConstraint
from sqlglot import exp
from sqlscope import Catalog
from sqlscope.catalog.constraint import ConstraintType
from ...exceptions import ConstraintMergeError, ConstraintValidationError
from collections import Counter

class MinTables(SchemaConstraint):
    '''Requires the schema to have a specific number of tables.'''

    def __init__(self, min_tables: int = 5) -> None:
        self.min_tables = min_tables

    def validate(self, catalog: Catalog, tables_sql: list[exp.Create], values_sql: list[exp.Insert]) -> None:
        table_count = len(tables_sql)

        if table_count < self.min_tables:
            raise ConstraintValidationError(f'Schema has {table_count} tables, which is less than the required minimum of {self.min_tables} tables.')

    @property
    def description(self) -> str:
        return f'Schema must be comprised of at least {self.min_tables} tables'
    
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
                raise ConstraintValidationError(f'Schema has {total_checks} CHECK constraints, which is less than the required minimum of {self.min}.')
        else:
            if not (self.min <= total_checks <= self.max):
                raise ConstraintValidationError(f'Schema has {total_checks} CHECK constraints, which is not within the required range of {self.min} to {self.max}.')
        
    @property
    def description(self) -> str:
        if self.max is None: 
            return f'Schema must have minimum {self.min} CHECK constraints'
        elif self.min == self.max: 
            return f'Schema must have exactly {self.min} CHECK constraints'
        else: 
            return f'Schema must have between {self.min} and {self.max} CHECK constraints'
        
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
            raise ConstraintValidationError(f'Schema has {valid_tables_count} tables with at least {self.columns} columns, which is less than the required minimum of {self.tables} tables.')

    @property
    def description(self) -> str:
        return f'Schema must have at least {self.tables} tables with at least {self.columns} columns'

    def merge(self, other: SchemaConstraint) -> 'MinColumns':
        if not isinstance(other, MinColumns):
            raise ConstraintMergeError(self, other)
        
        # Merging by taking the maximum of min_tables and min_columns
        merged_min_tables = max(self.tables, other.tables)
        merged_min_columns = max(self.columns, other.columns)

        return MinColumns(
            tables=merged_min_tables,
            columns=merged_min_columns
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
                f'Schema has {len(complex_cols_found)} columns with complex names ({complex_cols_found}), '
                f'which is less than the required minimum of {self.min_columns}.'
            )
    
    @property
    def description(self) -> str:
        return f'Schema must have at least {self.min_columns} columns with complex and lengthy names (length >= 15 and containing "_")'
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


        import dav_tools
        dav_tools.messages.debug(f'Column name counts across tables: {name_counts}')

        tables_with_same_col_names = sum(1 for count in name_counts.values() if count >= 2)
        if tables_with_same_col_names < self.pairs:
            raise ConstraintValidationError(
                f'Schema has {tables_with_same_col_names} pair(s) of non-key columns with the same name, '
                f'which is less than the required minimum of {self.pairs} pair(s).'
                f'Current column name counts: {name_counts}. Columns not counted are part of PKs/FKs.'
            )
    
    @property
    def description(self) -> str:
        return f'In CREATE TABLE must have at least {self.pairs} pair(s) of non-key columns (either PKs or FKs) with the same name'

    def merge(self, other: SchemaConstraint) -> 'SameColumnNames':
        if not isinstance(other, SameColumnNames):
            raise ConstraintMergeError(self, other)
        
        min_tables = max(self.pairs, other.pairs)
        return SameColumnNames(pairs=min_tables)