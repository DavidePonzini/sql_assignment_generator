import pytest
import sqlglot
from sqlscope import build_catalog_from_sql
from sql_assignment_generator.exceptions import ConstraintValidationError
from sql_assignment_generator.constraints.schema.tables import (
    MinTables, 
    MinChecks, 
    MinColumns, 
    ComplexColumnName, 
    SameColumnNames
)

# Helper function to prepare the environment for validation
def prepare_schema(create_sqls: list[str]):
    tables_ast = [sqlglot.parse_one(sql, read="postgres") for sql in create_sqls]
    # Build catalog to provide metadata about PKs, FKs, and columns
    catalog = build_catalog_from_sql("; ".join(create_sqls))
    # values_sql is not used by these specific constraints but required by the signature
    return catalog, tables_ast, []

# =================================================================
# TEST MIN TABLES PASS
# =================================================================

@pytest.mark.parametrize("create_sqls, min_val", [
    (["CREATE TABLE t1 (id INT PRIMARY KEY)", "CREATE TABLE t2 (id INT PRIMARY KEY)"], 2),
    (["CREATE TABLE t1 (id INT PRIMARY KEY)", "CREATE TABLE t2 (id INT PRIMARY KEY)", "CREATE TABLE t3 (id INT PRIMARY KEY)"], 2),
])

def test_min_tables_pass(create_sqls, min_val):
    catalog, tables_ast, values_ast = prepare_schema(create_sqls)
    constraint = MinTables(min_tables=min_val)
    constraint.validate(catalog, tables_ast, values_ast)

# =================================================================
# TEST MIN TABLES FAIL
# =================================================================

@pytest.mark.parametrize("create_sqls, min_val", [
    (["CREATE TABLE t1 (id INT PRIMARY KEY)"], 2),
])

def test_min_tables_fail(create_sqls, min_val):
    catalog, tables_ast, values_ast = prepare_schema(create_sqls)
    constraint = MinTables(min_tables=min_val)
    with pytest.raises(ConstraintValidationError):
        constraint.validate(catalog, tables_ast, values_ast)


# =================================================================
# TEST MIN CHECKS PASS
# =================================================================

@pytest.mark.parametrize("create_sqls, min_val", [
    (["CREATE TABLE t1 (id INT PRIMARY KEY CHECK (id > 0), val INT, CONSTRAINT c1 CHECK (val < 10))"], 2), # 1 column check + 1 table check = 2
    (["CREATE TABLE t1 (a INT PRIMARY KEY CHECK(a > 0))", "CREATE TABLE t2 (b INT PRIMARY KEY CHECK(b > 0))"], 2), # Check in different tables
])

def test_min_checks_pass(create_sqls, min_val):
    catalog, tables_ast, values_ast = prepare_schema(create_sqls)
    constraint = MinChecks(min_=min_val)
    constraint.validate(catalog, tables_ast, values_ast)

# =================================================================
# TEST MIN CHECKS FAIL
# =================================================================

def test_min_checks_fail():
    create_sqls = ["CREATE TABLE t1 (id INT PRIMARY KEY)"]
    catalog, tables_ast, values_ast = prepare_schema(create_sqls)
    constraint = MinChecks(min_=1)
    with pytest.raises(ConstraintValidationError):
        constraint.validate(catalog, tables_ast, values_ast)


# =================================================================
# TEST MIN COLUMNS PASS
# =================================================================

@pytest.mark.parametrize("create_sqls, cols, tabs", [
    (["CREATE TABLE t1 (a INT PRIMARY KEY, b INT, c INT)"], 2, 1), # 1 table with 3 columns, looking for 1 table with at least 2 columns
    (["CREATE TABLE t1 (a INT PRIMARY KEY, b INT)", "CREATE TABLE t2 (x INT PRIMARY KEY, y INT)"], 2, 2), # 2 tables with 2 columns each, looking for 2 tables with at least 2 columns
])

def test_min_columns_pass(create_sqls, cols, tabs):
    catalog, tables_ast, values_ast = prepare_schema(create_sqls)
    constraint = MinColumns(columns=cols, tables=tabs)
    constraint.validate(catalog, tables_ast, values_ast)

# =================================================================
# TEST MIN COLUMNS FAIL
# =================================================================

def test_min_columns_fail():
    create_sqls = ["CREATE TABLE t1 (a INT PRIMARY KEY, b INT, c INT)", "CREATE TABLE t2 (a INT PRIMARY KEY)"] # Only 1 table has 3 columns, but we require 2 tables to have 3 columns
    catalog, tables_ast, values_ast = prepare_schema(create_sqls)
    constraint = MinColumns(columns=3, tables=2)
    with pytest.raises(ConstraintValidationError):
        constraint.validate(catalog, tables_ast, values_ast)


# =================================================================
# TEST COMPLEX COLUMN NAME PASS
# =================================================================

@pytest.mark.parametrize("create_sqls", [
    ["CREATE TABLE t1 (this_is_a_very_long_name INT PRIMARY KEY)"], # length 23, has underscore
    ["CREATE TABLE t1 (first_col INT PRIMARY KEY, a_long_identifier_name VARCHAR(10))"]
])

def test_complex_column_name_pass(create_sqls):
    catalog, tables_ast, values_ast = prepare_schema(create_sqls)
    constraint = ComplexColumnName(min_columns=1)
    constraint.validate(catalog, tables_ast, values_ast)

# =================================================================
# TEST COMPLEX COLUMN NAME FAIL
# =================================================================

def test_complex_column_name_fail():
    create_sqls = ["CREATE TABLE t1 (short_name INT PRIMARY KEY, LongNameWithoutUnderscore INT)"] # "short_name" is under 15 chars, "LongNameWithoutUnderscore" has no '_'
    catalog, tables_ast, values_ast = prepare_schema(create_sqls)
    constraint = ComplexColumnName(min_columns=1)
    with pytest.raises(ConstraintValidationError):
        constraint.validate(catalog, tables_ast, values_ast)


# =================================================================
# TEST SAME COLUMN NAMES PASS
# =================================================================

@pytest.mark.parametrize("create_sqls, pairs", [
    ([
        "CREATE TABLE t1 (id INT PRIMARY KEY, status VARCHAR(10))", 
        "CREATE TABLE t2 (id INT PRIMARY KEY, status VARCHAR(10))"
    ], 1), # "status" is a non-key column in both tables
    ([
        "CREATE TABLE t1 (id INT PRIMARY KEY, created_at TIMESTAMP, updated_at TIMESTAMP)", 
        "CREATE TABLE t2 (uid INT PRIMARY KEY, created_at TIMESTAMP, updated_at TIMESTAMP)"
    ], 2) # "created_at" and "updated_at" are shared
])

def test_same_column_names_pass(create_sqls, pairs):
    catalog, tables_ast, values_ast = prepare_schema(create_sqls)
    constraint = SameColumnNames(pairs=pairs)
    constraint.validate(catalog, tables_ast, values_ast)

# =================================================================
# TEST SAME COLUMN NAMES FAIL
# =================================================================

def test_same_column_names_fail():
    # "id" is part of Primary Key or Foreign Key, should not be counted
    create_sqls = [
        "CREATE TABLE t1 (id INT PRIMARY KEY, val INT)",
        "CREATE TABLE t2 (other_id INT PRIMARY KEY, id INT REFERENCES t1(id))"
    ]
    catalog, tables_ast, values_ast = prepare_schema(create_sqls)
    constraint = SameColumnNames(pairs=1)
    with pytest.raises(ConstraintValidationError):
        constraint.validate(catalog, tables_ast, values_ast)