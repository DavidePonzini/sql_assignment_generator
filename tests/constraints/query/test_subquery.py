import pytest
from sqlscope import Query
from sql_assignment_generator.constraints.query.subquery import NoSubquery, Subqueries, NestedSubqueries, NoNesting
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
    "SELECT a, (SELECT b FROM t2 LIMIT 1) FROM t1", # Subquery in SELECT
    "SELECT a FROM t1 WHERE x = 1 GROUP BY a HAVING COUNT(*) > (SELECT AVG(count) FROM t)" # Subquery in HAVING
])

def test_no_subquery_fail(sql):
    query = Query(sql)
    constraint = NoSubquery()
    with pytest.raises(ConstraintValidationError) as exc_info:
        constraint.validate(query)

# =================================================================
# TEST NO NESTING PASS
# =================================================================
@pytest.mark.parametrize("sql", [
    "SELECT * FROM t WHERE id IN (SELECT id FROM t2)", # 1 subquery, no nesting
    "SELECT * FROM t WHERE id IN (SELECT id FROM t2) AND x > ALL (SELECT x FROM t3)", # 2 subqueries, no nesting
    "SELECT * FROM (SELECT id FROM t1) AS sub", # 1 subquery in FROM, no nesting
    "SELECT a, (SELECT b FROM t2 LIMIT 1) FROM t1", # 1 subquery in SELECT, no nesting
    "SELECT a FROM t1 WHERE x = 1 GROUP BY a HAVING COUNT(*) > (SELECT AVG(count) FROM t)" # 1 subquery in HAVING, no nesting
])
def test_no_nesting_pass(sql):
    query = Query(sql)
    constraint = NoNesting()
    constraint.validate(query)

# =================================================================
# TEST NO NESTING FAIL
# =================================================================

@pytest.mark.parametrize("sql", [
    "SELECT * FROM t WHERE id IN (SELECT id FROM t2 WHERE x IN (SELECT x FROM t3))", # 2 subqueries, 1 nesting
    "SELECT * FROM t WHERE id IN (SELECT id FROM t2) AND x > ALL (SELECT x FROM t3) AND id IN (SELECT id FROM t4 WHERE x > ANY (SELECT x FROM t5))", # 3 subqueries, 1 nesting (t4 contains nested t5)
    "SELECT a FROM t1 WHERE x = 1 GROUP BY a HAVING COUNT(*) > (SELECT AVG(count) FROM t WHERE y IN (SELECT y FROM t2))" # 2 subqueries, 1 nesting (subquery in HAVING contains nested subquery in WHERE)
])
def test_no_nesting_fail(sql):
    query = Query(sql)
    constraint = NoNesting()
    with pytest.raises(ConstraintValidationError) as exc_info:
        constraint.validate(query)


# =================================================================
# TEST SUBQUERIES PASS
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2)", 1, None), # 1 unnested subquery, min 1 required
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2) AND id IN (SELECT id FROM t3)", 1, 2), # 2 unnested subqueries at the same level, range 1-2
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2) AND id IN (SELECT id FROM t3 WHERE x > ANY (SELECT x FROM t4))", 1, 2), # 2 unnested subqueries at the same level, range 1-2. The subquery in t3 is nested, but that doesn't affect the count of unnested subqueries at the same level.
    ("SELECT * FROM (SELECT id FROM t1) AS sub", 1, None), # 1 unnested subquery in FROM, min 1
    ("SELECT * FROM (SELECT id FROM t1) AS sub WHERE id IN (SELECT id FROM t2) AND x > ALL (SELECT x FROM t3)", 2, None), # 2 unnested subqueries at second level (in WHERE), min 2
    ("SELECT * FROM t1 WHERE x = (SELECT MAX(x) FROM t2)", 1, 1), # 1 subquery, exactly 1 required
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2) AND id IN (SELECT id FROM t3) OR id IN (SELECT 1)", 3, 3), # 3 unnested subqueries at the same level
])

def test_unnested_subqueries_pass(sql, min_, max_):
    query = Query(sql)
    constraint = Subqueries(min_=min_, max_=max_)
    constraint.validate(query)

# =================================================================
# TEST SUBQUERIES FAIL
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    
    ("SELECT * FROM t1", 1, None), # No subqueries at all, min 1 required
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2 WHERE x IN (SELECT x FROM t3))", 2, None),  # Two subqueries found, but both are nested inside the same SELECT, so no SELECT has 2 unnested subqueries at the same level, min 2 required
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2) AND id IN (SELECT id FROM t3) OR id IN (SELECT 1)", 1, 1), # 2 unnested subqueries found, but max 1 required
])

def test_unnested_subqueries_fail(sql, min_, max_):
    query = Query(sql)
    constraint = Subqueries(min_=min_, max_=max_)
    with pytest.raises(ConstraintValidationError) as exc_info:
        constraint.validate(query)


# =================================================================
# TEST NESTED SUBQUERIES PASS
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2 WHERE x IN (SELECT x FROM t3))", 1, 1), # 2 nested subqueries (total 2 SELECTs excluding root), min 2
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2 WHERE x > ALL (SELECT 1)) AND id IN (SELECT id FROM t3 WHERE x > ANY (SELECT x FROM t4))", 2, 2),  # 2 nestings (t2 contains nested t3, and t3 contains nested t4), min 2, no max
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2) AND x > ALL (SELECT x FROM t3) AND id IN (SELECT id FROM t4 WHERE x > ANY (SELECT x FROM t5))", 1, 1), # 1 nesting (t4 contains nested t5), min 1, no max. The subqueries in t2
])

def test_nested_subqueries_pass(sql, min_, max_):
    query = Query(sql)
    constraint = NestedSubqueries(min_=min_, max_=max_)
    constraint.validate(query)

# =================================================================
# TEST NESTED SUBQUERIES FAIL
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT * FROM t1", 1, None), # No subqueries, min 1 required
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2)", 2, None), # 1 subquery found, but 2 required
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2) AND id IN (SELECT id FROM t3)", 1, 1), # 2 subqueries found, but max 1 allowed
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2 WHERE x IN (SELECT x FROM t3))", 2, None) # 2 nestings required, only 1 nesting found (t3 is nested inside t2, but there are no other subqueries at the same level as t2 that contain nested subqueries)
])

def test_nested_subqueries_fail(sql, min_, max_):
    query = Query(sql)
    constraint = NestedSubqueries(min_=min_, max_=max_)
    with pytest.raises(ConstraintValidationError) as exc_info:
        constraint.validate(query)