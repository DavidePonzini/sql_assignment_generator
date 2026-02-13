import pytest
from sqlscope import Query
from sql_assignment_generator.constraints.query.subquery import NoSubquery, UnnestedSubqueries, Subqueries
from sql_assignment_generator.exceptions import ConstraintValidationError

# =================================================================
# TEST NO SUBQUERY PASS
# =================================================================

@pytest.mark.parametrize("sql", [
    "SELECT * FROM t",
    "SELECT a, b FROM t1 JOIN t2 ON t1.id = t2.id",
    "SELECT COUNT(*) FROM t GROUP BY a"
])

def test_no_subquery_pass(sql):
    query = Query(sql)
    constraint = NoSubquery()
    constraint.validate(query)

# =================================================================
# TEST NO SUBQUERY FAIL
# =================================================================

@pytest.mark.parametrize("sql", [
    "SELECT * FROM t WHERE id IN (SELECT id FROM t2)", # Subquery in WHERE
    "SELECT * FROM (SELECT id FROM t) AS sub", # Subquery in FROM
    "SELECT a, (SELECT b FROM t2 LIMIT 1) FROM t1" # Subquery in SELECT
])

def test_no_subquery_fail(sql):
    query = Query(sql)
    constraint = NoSubquery()
    with pytest.raises(ConstraintValidationError) as exc_info:
        constraint.validate(query)
    assert "Subqueries were detected" in str(exc_info.value)

# =================================================================
# TEST UNNESTED SUBQUERIES PASS
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2)", 1, None), # 1 unnested subquery, min 1 required
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2) AND id IN (SELECT id FROM t3)", 1, 2), # 2 unnested subqueries at the same level, range 1-2
    ("SELECT * FROM (SELECT id FROM t1) AS sub", 1, None), # 1 unnested subquery in FROM, min 1
    ("SELECT * FROM t1 WHERE x = (SELECT MAX(x) FROM t2)", 1, 1), # 1 subquery, exactly 1 required
])

def test_unnested_subqueries_pass(sql, min_, max_):
    query = Query(sql)
    constraint = UnnestedSubqueries(min_=min_, max_=max_)
    constraint.validate(query)

# =================================================================
# TEST UNNESTED SUBQUERIES FAIL
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    
    ("SELECT * FROM t1", 1, None), # No subqueries at all, min 1 required
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2 WHERE x IN (SELECT x FROM t3))", 1, None),  # Nested subqueries (Sub-subquery), should be rejected by the nesting check
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2) AND id IN (SELECT id FROM t3)", 1, 1), # 2 unnested subqueries found, but max 1 required
])

def test_unnested_subqueries_fail(sql, min_, max_):
    query = Query(sql)
    constraint = UnnestedSubqueries(min_=min_, max_=max_)
    with pytest.raises(ConstraintValidationError) as exc_info:
        constraint.validate(query)


# =================================================================
# TEST SUBQUERIES (NESTED OR UNNESTED) PASS
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2)", 1, None), # 1 unnested subquery, min 1
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2 WHERE x IN (SELECT x FROM t3))", 2, 2), # 2 nested subqueries (total 2 SELECTs excluding root), min 2
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2) AND id IN (SELECT id FROM t3)", 2, None)# Exactly 2 subqueries (nested or not)
])

def test_subqueries_pass(sql, min_, max_):
    query = Query(sql)
    constraint = Subqueries(min_=min_, max_=max_)
    constraint.validate(query)

# =================================================================
# TEST SUBQUERIES FAIL
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT * FROM t1", 1, None), # No subqueries, min 1 required
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2)", 2, None), # 1 subquery found, but 2 required
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2) AND id IN (SELECT id FROM t3)", 1, 1) # 2 subqueries found, but max 1 allowed
])

def test_subqueries_fail(sql, min_, max_):
    query = Query(sql)
    constraint = Subqueries(min_=min_, max_=max_)
    with pytest.raises(ConstraintValidationError) as exc_info:
        constraint.validate(query)
    assert "required number of subqueries" in str(exc_info.value)