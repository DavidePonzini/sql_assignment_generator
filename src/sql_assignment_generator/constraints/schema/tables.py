from .base import SchemaConstraint
from sqlglot import exp
from sqlscope import Catalog
from sqlscope.catalog.constraint import ConstraintType
from ...exceptions import ConstraintMergeError
from collections import Counter

class MinTables(SchemaConstraint):
    '''Requires the schema to have a specific number of tables.'''

    def __init__(self, min_tables: int = 5) -> None:
        self.min_tables = min_tables

    def validate(self, catalog: Catalog, tables_sql: list[exp.Create], values_sql: list[exp.Insert]) -> bool:
        table_count = len(tables_sql)
        return self.min_tables <= table_count

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

    def validate(self, catalog: Catalog, tables_sql: list[exp.Create], values_sql: list[exp.Insert]) -> bool:
        total_checks = 0
        
        for table in tables_sql:
            checks_found = list(table.find_all(exp.Check, exp.CheckColumnConstraint))
            total_checks += len(checks_found)

        if self.max is None:
            return total_checks >= self.min
        return self.min <= total_checks <= self.max
        
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

    def validate(self, catalog: Catalog, tables_sql: list[exp.Create], values_sql: list[exp.Insert]) -> bool:
        valid_tables_count = 0

        for schema_name in catalog.schema_names:
            for table_name in catalog[schema_name].table_names:
                table = catalog[schema_name][table_name]
                
                # count columns in the table
                column_count = len(table.columns)
                
                # if column count meets the minimum, increment valid table count
                if column_count >= self.columns:
                    valid_tables_count += 1
        
        return valid_tables_count >= self.tables

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

    def validate(self, catalog: Catalog, tables_sql: list[exp.Create], values_sql: list[exp.Insert]) -> bool:
        complex_cols_found = 0

        for schema_name in catalog.schema_names:
            for table_name in catalog[schema_name].table_names:
                table = catalog[schema_name][table_name]
                
                for column in table.columns:
                    col_name = column.real_name
                    
                    # check criteria
                    if len(col_name) >= 15 and '_' in col_name:
                        complex_cols_found += 1

        return complex_cols_found >= self.min_columns
    
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

    def __init__(self, min_tables: int = 1) -> None:
        if min_tables < 2:
            min_tables = 2
        self.min_tables = min_tables

    def validate(self, catalog: Catalog, tables_sql: list[exp.Create], values_sql: list[exp.Insert]) -> bool:
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
                    if col_name in pk_cols:
                        continue

                    name_counts[col_name] += 1

        tables_with_same_col_names = sum(1 for count in name_counts.values() if count >= 2)
        return tables_with_same_col_names >= self.min_tables
    
    @property
    def description(self) -> str:
        return f'In CREATE TABLE must have at least {self.min_tables} tables with non-key columns (either PKs or FKs) with the same name'

    def merge(self, other: SchemaConstraint) -> 'SameColumnNames':
        if not isinstance(other, SameColumnNames):
            raise ConstraintMergeError(self, other)
        
        min_tables = max(self.min_tables, other.min_tables)
        return SameColumnNames(min_tables=min_tables)