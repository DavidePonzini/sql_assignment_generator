import pytest
import sqlglot
from sqlglot import exp
from sqlscope import build_catalog_from_sql
from sql_assignment_generator.constraints.schema.values import MinRows
from sql_assignment_generator.exceptions import ConstraintValidationError

from . import prepare_catalog

# =================================================================
# TEST MIN ROWS PASS
# =================================================================

@pytest.mark.parametrize("create_sqls, insert_sqls, min_val", [
    (["CREATE TABLE t1 (id INT PRIMARY KEY)"], ["INSERT INTO t1 (id) VALUES (1), (2), (3)"], 3), # Single table with exactly 3 rows
    (
        ["CREATE TABLE t1 (id INT PRIMARY KEY)", "CREATE TABLE t2 (id INT PRIMARY KEY)"],
        ["INSERT INTO t1 (id) VALUES (1), (2), (3)", "INSERT INTO t2 (id) VALUES (10), (20), (30), (40)"],
        3
    ), # Multiple tables both satisfying the minimum
    
    (
        ["CREATE TABLE t1 (id INT PRIMARY KEY)"],
        ["INSERT INTO t1 (id) VALUES (1)", "INSERT INTO t1 (id) VALUES (2), (3)"], 
        3
    ),# Multiple INSERT statements for the same table (aggregation check)
    (["CREATE TABLE t1 (id INT PRIMARY KEY)"], [], 0) # Minimum is 0, no data needed
])

def test_min_rows_pass(create_sqls, insert_sqls, min_val):
    catalog, tables_ast, values_ast = prepare_catalog(create_sqls, insert_sqls)
    constraint = MinRows(min_=min_val)
    constraint.validate(catalog, tables_ast, values_ast)


# =================================================================
# TEST MIN ROWS FAIL
# =================================================================

@pytest.mark.parametrize("create_sqls, insert_sqls, min_val", [
    # Table has only 2 rows, 3 required
    (
        ["CREATE TABLE t1 (id INT PRIMARY KEY)"],
        ["INSERT INTO t1 (id) VALUES (1), (2)"],
        3
    ),
    # One table passes, but the other fails
    (
        ["CREATE TABLE t1 (id INT PRIMARY KEY)", "CREATE TABLE t2 (id INT PRIMARY KEY)"],
        ["INSERT INTO t1 (id) VALUES (1), (2), (3)", "INSERT INTO t2 (id) VALUES (1)"],
        3
    ),
    # No rows found at all, but min > 0
    (
        ["CREATE TABLE t1 (id INT PRIMARY KEY)"],
        [],
        1
    )
])

def test_min_rows_fail(create_sqls, insert_sqls, min_val):
    catalog, tables_ast, values_ast = prepare_catalog(create_sqls, insert_sqls)
    constraint = MinRows(min_=min_val)
    with pytest.raises(ConstraintValidationError):
        constraint.validate(catalog, tables_ast, values_ast)


# =================================================================
# TEST MIN ROWS MERGE
# =================================================================

def test_min_rows_merge():
    c1 = MinRows(min_=3)
    c2 = MinRows(min_=5)
    merged = c1.merge(c2)
    
    assert merged.min == 5
    assert isinstance(merged, MinRows)