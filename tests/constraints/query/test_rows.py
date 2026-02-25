import pytest
from sqlscope import Query
from sql_assignment_generator.constraints.query.rows import (
    Duplicates, 
    NoDuplicates, 
    Distinct
)
from sql_assignment_generator.exceptions import ConstraintValidationError

# =================================================================
# TEST DUPLICATES PASS
# =================================================================

@pytest.mark.parametrize("sql", [
    "SELECT a FROM t", # Standard column (not unique)
    "SELECT a, b FROM t WHERE b > 20 ORDER BY a",  # Multiple non-unique columns
    "SELECT a FROM (SELECT * FROM t) AS sub", #main query doesn't have unique constraints
    "SELECT * FROM (SELECT a FROM t) AS sub", # Main query forces uniqueness on subquery results
])

def test_duplicates_pass(sql):
    query = Query(sql)
    constraint = Duplicates()
    constraint.validate(query)

# =================================================================
# TEST DUPLICATES FAIL
# =================================================================

@pytest.mark.parametrize("sql", [
    "SELECT DISTINCT a FROM t", # DISTINCT forces uniqueness
    "SELECT a, COUNT(*) FROM t GROUP BY a", # GROUP BY forces uniqueness
    "SELECT a FROM (SELECT DISTINCT a FROM t) AS sub", # Main query has no grouping/distinct even if subquery does
    "SELECT DISTINCT * FROM (SELECT a FROM t) AS sub", # Main query forces uniqueness on subquery results
])
def test_duplicates_fail(sql):
    query = Query(sql)
    constraint = Duplicates()
    with pytest.raises(ConstraintValidationError):
        constraint.validate(query)

# =================================================================
# TEST NO DUPLICATES PASS
# =================================================================

@pytest.mark.parametrize("sql", [
    "SELECT a, AVG(b) FROM t GROUP BY a", # GROUP BY satisfies the 'other than DISTINCT' requirement
    "SELECT sub.id FROM (SELECT id FROM t) AS sub GROUP BY sub.id" # Subquery with group by in the main query
])

def test_no_duplicates_pass(sql):
    query = Query(sql)
    constraint = NoDuplicates()
    constraint.validate(query)

# =================================================================
# TEST NO DUPLICATES FAIL
# =================================================================

@pytest.mark.parametrize("sql", [
    "SELECT a FROM t", # No unique constraint
    "SELECT DISTINCT a FROM t", # DISTINCT is filtered out by the logic
    "SELECT * FROM (SELECT a FROM t) AS sub"
])
def test_no_duplicates_fail(sql):
    query = Query(sql)
    constraint = NoDuplicates()
    with pytest.raises(ConstraintValidationError):
        constraint.validate(query)


# =================================================================
# TEST DISTINCT PASS
# =================================================================

@pytest.mark.parametrize("sql", [
    "SELECT DISTINCT a FROM t", # Global DISTINCT
    "SELECT DISTINCT sub.a FROM (SELECT a FROM t) AS sub", # DISTINCT in the main query selecting from a subquery
    "SELECT DISTINCT a FROM t GROUP BY a, b", # DISTINCT with GROUP BY, but only one grouping column is selected, so DISTINCT is still necessary to ensure uniqueness
])

def test_distinct_pass(sql):
    query = Query(sql)
    constraint = Distinct()
    constraint.validate(query)

# =================================================================
# TEST DISTINCT FAIL
# =================================================================

@pytest.mark.parametrize("sql", [
    "SELECT a FROM t", # No DISTINCT
    "SELECT DISTINCT a FROM t GROUP BY a", # even without DISTINCT, the query returns unique rows due to GROUP BY
    "SELECT a FROM (SELECT DISTINCT a FROM t) AS sub", # DISTINCT is only in the subquery, not the main query
    "SELECT a FROM t1 WHERE id IN (SELECT DISTINCT id FROM t2)", # Complex query but still missing DISTINCT
])

def test_distinct_fail(sql):
    query = Query(sql)
    constraint = Distinct()
    with pytest.raises(ConstraintValidationError):
        constraint.validate(query)