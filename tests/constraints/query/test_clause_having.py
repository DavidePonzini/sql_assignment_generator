import pytest
from sqlscope import Query
from sql_assignment_generator.constraints.query.clause_having import NoHaving, Having
from sql_assignment_generator.exceptions import ConstraintValidationError

# =================================================================
# TEST NO HAVING PASS
# =================================================================

@pytest.mark.parametrize("sql", [
    "SELECT * FROM t",
    "SELECT a, COUNT(*) FROM t WHERE a > 10",
    "SELECT * FROM t1 WHERE id IN (SELECT id FROM t2 WHERE id < 5)" 
])

def test_no_having_pass(sql):
    query = Query(sql)
    constraint = NoHaving()
    constraint.validate(query)

# =================================================================
# TEST NO HAVING FAIL
# =================================================================

@pytest.mark.parametrize("sql", [
    "SELECT a, COUNT(*) FROM t GROUP BY a HAVING COUNT(*) > 1",
    "SELECT a, AVG(b) FROM t GROUP BY a HAVING AVG(b) > 10 AND SUM(c) < 100",
    "SELECT * FROM t1 WHERE id IN (SELECT id FROM t2 GROUP BY id HAVING COUNT(*) > 1)",
    "SELECT id FROM t1 WHERE id IN (SELECT id FROM t2) GROUP BY id HAVING COUNT(*) > 1"
])

def test_no_having_fail(sql):
    query = Query(sql)
    constraint = NoHaving()
    with pytest.raises(ConstraintValidationError) as exc_info:
        constraint.validate(query)

# =================================================================
# TEST HAVING PASS
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT a FROM t GROUP BY a HAVING COUNT(*) > 1 AND AVG(b) < 10", 2, None), # 2 condition and min 2 condition require
    ("SELECT a FROM t GROUP BY a HAVING SUM(c) > 0 OR MIN(d) = 1", 1, 2), # 1 condition and range 1-2 condition require
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2 GROUP BY id HAVING COUNT(*) > 5)", 1, None), # 1 condition in subquery and min 1 condition require
    ("SELECT a FROM t GROUP BY a HAVING c1 > 0 AND c2 < 10 OR c3 = 5", 3, 3), # 3 condition and exactly 3 condition require
    ("SELECT id FROM t1 WHERE id IN (SELECT id FROM t2) GROUP BY id HAVING COUNT(*) > 1", 1, 1)# 1 condition out of subquery and exactly 1 condition require
])

def test_having_pass(sql, min_, max_):
    query = Query(sql)
    constraint = Having(min_=min_, max_=max_)
    constraint.validate(query)

# =================================================================
# TEST HAVING FAIL
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT a, COUNT(*) FROM t GROUP BY a", 1, None), # no HAVING
    ("SELECT a FROM t GROUP BY a HAVING COUNT(*) > 1", 2, None),  # 1 condition but require minimum 2
    ("SELECT a FROM t GROUP BY a HAVING c1 > 0 AND c2 < 10", 1, 1), # 2 condition but require maximum 1
    ("SELECT a FROM t GROUP BY a HAVING c1 > 0 OR c2 < 10", 3, 5), # 2 condition but require range 3-5
])

def test_having_fail(sql, min_, max_):
    query = Query(sql)
    constraint = Having(min_=min_, max_=max_)
    with pytest.raises(ConstraintValidationError) as exc_info:
        constraint.validate(query)