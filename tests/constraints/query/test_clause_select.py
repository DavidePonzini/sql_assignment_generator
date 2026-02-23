import pytest
from sqlscope import Query
from sql_assignment_generator.constraints.query.clause_select import (
    SelectedColumns, 
    NoAlias, 
    Alias
)
from sql_assignment_generator.exceptions import ConstraintValidationError

# =================================================================
# TEST SELECTED COLUMNS PASS
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT col1, col2 FROM t", 2, None), # 2 columns, min 2 required
    ("SELECT col1, col2 FROM t", 1, 2), # 2 columns, range 1-2 required
    ("SELECT col1, col2, col3 FROM t", 3, 3), # 3 columns, exactly 3 required
    ("SELECT a FROM t1 WHERE id IN (SELECT id, b FROM t2)", 1, 1) # 1 columns in main select, exactly 1 column required
])

def test_selected_columns_pass(sql, min_, max_):
    query = Query(sql)
    constraint = SelectedColumns(min_=min_, max_=max_)
    constraint.validate(query)

# =================================================================
# TEST SELECTED COLUMNS FAIL
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT * FROM t", 1, None), # all column found, but exactly one required
    ("SELECT col1 FROM t", 2, None), # 1 found, but 2 required
    ("SELECT col1, col2, col3 FROM t", 1, 2), # 3 found, but max 2 allowed
    ("SELECT col1, col2 FROM t", 3, 3), # 2 found, but exactly 3 required
    ("SELECT a, b FROM t1 WHERE id = (SELECT id FROM t2)", 1, 1) # 2 column found in main select, but exactly 1 required
])

def test_selected_columns_fail(sql, min_, max_):
    query = Query(sql)
    constraint = SelectedColumns(min_=min_, max_=max_)
    with pytest.raises(ConstraintValidationError):
        constraint.validate(query)


# =================================================================
# TEST NO ALIAS PASS
# =================================================================

@pytest.mark.parametrize("sql", [
    "SELECT col1 FROM t",
    "SELECT col1, col2 FROM t",
    "SELECT t.col1, t.col2 FROM t",
    "SELECT a FROM (SELECT a AS n FROM t) AS sub" #there are no alias in main select column
])

def test_no_alias_pass(sql):
    query = Query(sql)
    constraint = NoAlias()
    constraint.validate(query)

# =================================================================
# TEST NO ALIAS FAIL
# =================================================================

@pytest.mark.parametrize("sql", [
    "SELECT col1 AS alias1 FROM t", # Explicit AS alias
    "SELECT col1 alias1 FROM t", # Implicit alias
    "SELECT col1, col2 AS alias2 FROM t", # One of the columns is aliased
    "SELECT a, (SELECT AVG(b) FROM t1) AS b FROM t2" #there are alias in main select column
])

def test_no_alias_fail(sql):
    query = Query(sql)
    constraint = NoAlias()
    with pytest.raises(ConstraintValidationError):
        constraint.validate(query)


# =================================================================
# TEST ALIAS PASS
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT col1 AS a FROM t", 1, None), # 1 alias, min 1 required
    ("SELECT col1 AS a, col2 AS b FROM t", 2, None), # 2 aliases, min 2 required
    ("SELECT col1 AS a, col2 FROM t", 1, 1), # Exactly 1 alias
    ("SELECT col1 AS a, col2 AS b, col3 FROM t", 1, 2), # 2 aliases, range 1-2
    ("SELECT name AS n, (SELECT MAX(a) FROM t1) AS max FROM t2", 2, 2) # 2 aliases and exactly 2 require
])

def test_alias_pass(sql, min_, max_):
    query = Query(sql)
    constraint = Alias(min_=min_, max_=max_)
    constraint.validate(query)

# =================================================================
# TEST ALIAS FAIL
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT col1 FROM t", 1, None), # 0 aliases found, but 1 required
    ("SELECT col1 AS a FROM t", 2, None), # 1 alias found, but 2 required
    ("SELECT col1 AS a, col2 AS b FROM t", 1, 1), # 2 aliases found, but max 1 allowed
    ("SELECT col1 AS a, col2 AS b, col3 AS c FROM t", 1, 2), # 3 aliases found, but max 2 allowed
    ("SELECT a, (SELECT AVG(b) FROM t1) FROM t2", 2, 2) # 0 aliases and exactly 2 require
])

def test_alias_fail(sql, min_, max_):
    query = Query(sql)
    constraint = Alias(min_=min_, max_=max_)
    with pytest.raises(ConstraintValidationError):
        constraint.validate(query)