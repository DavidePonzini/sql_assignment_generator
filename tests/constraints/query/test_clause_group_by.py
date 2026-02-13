import pytest
from sqlscope import Query
from sql_assignment_generator.constraints.query.clause_group_by import NoGroupBy, GroupBy
from sql_assignment_generator.exceptions import ConstraintValidationError

# =================================================================
# TEST NO GROUP BY PASS
# =================================================================

@pytest.mark.parametrize("sql", [
    "SELECT * FROM t",
    "SELECT a, b FROM t WHERE c > 10",
    "SELECT s.name, c.name FROM t1 s JOIN t2 c ON s.id = c.id",
    "SELECT * FROM t1 WHERE id IN (SELECT id FROM t2)" 
])

def test_no_group_by_pass(sql):
    query = Query(sql)
    constraint = NoGroupBy()
    constraint.validate(query)

# =================================================================
# TEST NO GROUP BY FAIL
# =================================================================

@pytest.mark.parametrize("sql", [
    "SELECT id, COUNT(*) FROM t1 GROUP BY id",
    "SELECT id, a, AVG(b) FROM t1 GROUP BY id, a",
    "SELECT * FROM t1 WHERE id IN (SELECT id FROM t2 GROUP BY id)",
    "SELECT * FROM (SELECT x, SUM(y) FROM t GROUP BY x );"
])

def test_no_group_by_fail(sql):
    query = Query(sql)
    constraint = NoGroupBy()

    with pytest.raises(ConstraintValidationError) as exc_info:
        constraint.validate(query)

# =================================================================
# TEST GROUP BY PASS
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT id, COUNT(*) FROM t GROUP BY id", 1, None), # group by on 1 col and min 1 col require
    ("SELECT id, a, AVG(age) FROM t GROUP BY id, a", 2, None), #group by 2 col and min 2 col require
    ("SELECT id, a, AVG(age) FROM t GROUP BY id, a", 1, 2), #group by 2 col and range 1-2 col require
    ("SELECT id, COUNT(*) FROM t GROUP BY id", 1, 1), #group by 1 col and 1-1 col require
    ("SELECT name FROM t1 WHERE id IN (SELECT id FROM t2 GROUP BY id)", 1, None) #group by 1 col in subquery and min 1 col require
])

def test_group_by_pass(sql, min_, max_):
    query = Query(sql)
    constraint = GroupBy(min_=min_, max_=max_)
    constraint.validate(query)

# =================================================================
# TEST GROUP BY FAIL
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT * FROM students", 1, None), #no group by
    ("SELECT major_id, COUNT(*) FROM students GROUP BY major_id", 2, None), #group by of 1 column but required minimum 2
    ("SELECT major_id, gender, AVG(age) FROM students GROUP BY major_id, gender", 1, 1), #group by of 2 column but required maximum 2
    ("SELECT major_id, gender, AVG(age) FROM students GROUP BY major_id, gender", 3, 5), #group by of 2 column but required range 3-5
    ("SELECT name FROM t1 WHERE id IN (SELECT AVG(a), id FROM t2)", 1, None), #group by of 2 column but required range 3-5
    ("SELECT id, AVG(age) FROM t GROUP BY id", 3, 5) #group by is present but of 1 column with required range 3-5
])

def test_group_by_fail(sql, min_, max_):
    query = Query(sql)
    constraint = GroupBy(min_=min_, max_=max_)
    with pytest.raises(ConstraintValidationError) as exc_info:
        constraint.validate(query)
