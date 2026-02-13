import pytest
from sqlscope import Query
from sql_assignment_generator.constraints.query.clause_order_by import (
    NoOrderBy, 
    OrderBy, 
    OrderByASC, 
    OrderByDESC
)
from sql_assignment_generator.exceptions import ConstraintValidationError

# =================================================================
# TEST NO ORDER BY PASS
# =================================================================

@pytest.mark.parametrize("sql", [
    "SELECT * FROM t",
    "SELECT a, b FROM t WHERE b > 5000",
    "SELECT * FROM (SELECT id FROM t) AS a"
])

def test_no_order_by_pass(sql):
    query = Query(sql)
    constraint = NoOrderBy()
    constraint.validate(query)

# =================================================================
# TEST NO ORDER BY FAIL
# =================================================================

@pytest.mark.parametrize("sql", [
    "SELECT * FROM t ORDER BY a",
    "SELECT * FROM t ORDER BY a DESC",
    "SELECT * FROM t ORDER BY a ASC",
    "SELECT * FROM (SELECT id FROM t ORDER BY id) AS sub",
    "SELECT * FROM (SELECT id FROM t) AS sub ORDER BY id"
])

def test_no_order_by_fail(sql):
    query = Query(sql)
    constraint = NoOrderBy()
    with pytest.raises(ConstraintValidationError):
        constraint.validate(query)

# =================================================================
# TEST ORDER BY PASS
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT * FROM t ORDER BY col1", 1, None), # 1 column and min 1 required
    ("SELECT * FROM t ORDER BY col1, col2", 2, None), # 2 columns and min 2 required
    ("SELECT * FROM t ORDER BY col1, col2", 1, 2), # 2 columns and range 1-2 required
    ("SELECT * FROM t ORDER BY col1 ASC, col2 DESC", 2, 2), # Works even if mixed ASC/DESC
    ("SELECT * FROM (SELECT id FROM t ORDER BY id) AS sub", 1, 1), # 1 columns into subquery and exactly 1 required
])

def test_order_by_pass(sql, min_, max_):
    query = Query(sql)
    constraint = OrderBy(min_=min_, max_=max_)
    constraint.validate(query)

# =================================================================
# TEST ORDER BY FAIL
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT * FROM t", 1, None), # No ORDER BY found
    ("SELECT * FROM t ORDER BY col1", 2, None), # 1 column found but 2 required
    ("SELECT * FROM t ORDER BY c1, c2, c3", 1, 2), # 3 columns found but max 2 allowed
    ("SELECT * FROM (SELECT id FROM t ORDER BY id) AS sub", 2, None), # 1 columns into subquery and exactly 1 required
])

def test_order_by_fail(sql, min_, max_):
    query = Query(sql)
    constraint = OrderBy(min_=min_, max_=max_)
    with pytest.raises(ConstraintValidationError):
        constraint.validate(query)

# =================================================================
# TEST ORDER BY ASC PASS
# =================================================================

@pytest.mark.parametrize("sql", [
    "SELECT * FROM t ORDER BY col1", # Default is Ascending
    "SELECT * FROM t ORDER BY col1 ASC", # Explicit ASC
    "SELECT * FROM t ORDER BY col1 ASC, col2 DESC", # Mixture where 1 is ASC
    "SELECT * FROM (SELECT id FROM t ORDER BY id) AS sub", # ASC into subquery
])

def test_order_by_asc_pass(sql):
    query = Query(sql)
    constraint = OrderByASC()
    constraint.validate(query)

# =================================================================
# TEST ORDER BY ASC FAIL
# =================================================================

@pytest.mark.parametrize("sql", [
    "SELECT * FROM t", # Only DESC provided, 1 ASC required
    "SELECT * FROM t ORDER BY col1 DESC", # Only DESC provided, 1 ASC required
    "SELECT * FROM (SELECT id FROM t ORDER BY id DESC) AS sub", # NO ASC into subquery
])

def test_order_by_asc_fail(sql):
    query = Query(sql)
    constraint = OrderByASC()
    with pytest.raises(ConstraintValidationError):
        constraint.validate(query)

# =================================================================
# TEST ORDER BY DESC PASS
# =================================================================

@pytest.mark.parametrize("sql", [
    "SELECT * FROM t ORDER BY col1 DESC", # Explicit DESC
    "SELECT * FROM t ORDER BY c1 DESC, c2 DESC", # 2 DESC columns
    "SELECT * FROM t ORDER BY c1 ASC, c2 DESC", # 1 DESC among others
    "SELECT * FROM (SELECT id FROM t ORDER BY id DESC) AS sub", # DESC into subquery
])

def test_order_by_desc_pass(sql):
    query = Query(sql)
    constraint = OrderByDESC()
    constraint.validate(query)

# =================================================================
# TEST ORDER BY DESC FAIL
# =================================================================

@pytest.mark.parametrize("sql", [
    "SELECT * FROM t ORDER BY col1", # Default (ASC) does not count as DESC
    "SELECT * FROM t ORDER BY col1 ASC", # Explicit ASC does not count as DESC
    "SELECT * FROM t", # No ORDER BY at all
    "SELECT * FROM (SELECT id FROM t ORDER BY id) AS sub", # no DESC into subquery
])

def test_order_by_desc_fail(sql):
    query = Query(sql)
    constraint = OrderByDESC()
    with pytest.raises(ConstraintValidationError):
        constraint.validate(query)