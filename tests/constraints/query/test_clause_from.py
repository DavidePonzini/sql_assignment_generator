import pytest
from sqlscope import Query
from sql_assignment_generator.constraints.query.clause_from import (
    TableReferences, 
    LeftJoin, 
    RightJoin, 
    NoJoin, 
    SelfJoin
)
from sql_assignment_generator.exceptions import ConstraintValidationError

# =================================================================
# TEST TABLE REFERENCES FAIL
# =================================================================

@pytest.mark.parametrize("sql, min_, max_, allow_self", [
    ("SELECT * FROM t1", 2, None, False), # 1 table but minimum 2
    ("SELECT * FROM t1 JOIN t2 ON t1.id = t2.id", 1, 1, False), #2 table but max 1
    ("SELECT * FROM t1, t2 ON t1.id = t2.id", 1, 1, False), #2 table but max 1
    ("SELECT * FROM t1 WHERE id IN (SELECT x FROM t2 JOIN t3 ON t2.id = t3.id)", 1, 1, False), # subquery 2 table but max 1
])
def test_table_references_fail(sql, min_, max_, allow_self):
    query = Query(sql)
    constraint = TableReferences(min_=min_, max_=max_, allow_self_join=allow_self)
    with pytest.raises(ConstraintValidationError):
        constraint.validate(query)

# =================================================================
# TEST TABLE REFERENCES PASS
# =================================================================

@pytest.mark.parametrize("sql, min_, max_, allow_self", [
    ("SELECT * FROM t1", 1, 2, False), # 1 table and range 1-2
    ("SELECT * FROM t1 JOIN t2 ON t1.id = t2.id", 2, None, False), # 2 table in JOIN and min 2
    ("SELECT * FROM t1, t2 ", 2, None, False), # 2 table in JOIN and min 2 (cartesian product) ################################################################
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2)", 1, 1, False), # 2 total table and each block has 1 (Main=1, Sub=1)   ################################################
    ("SELECT * FROM t1 a JOIN t1 b ON a.id = b.pid", 2, 2, True), # Self join (t1 ripetuta), se allow_self_join=True conta 2 riferimenti
])
def test_table_references_pass(sql, min_, max_, allow_self):
    query = Query(sql)
    constraint = TableReferences(min_=min_, max_=max_, allow_self_join=allow_self)
    constraint.validate(query)

# =================================================================
# TEST LEFT JOIN PASS
# =================================================================

@pytest.mark.parametrize("sql", [
    "SELECT * FROM t1 LEFT JOIN t2 ON t1.id = t2.id",
    "SELECT * FROM t1 LEFT OUTER JOIN t2 ON t1.id = t2.id",
    "SELECT * FROM t1 JOIN t2 ON t1.id = t2.id LEFT JOIN t3 ON t2.id = t3.id",
    "SELECT * FROM t1 WHERE id IN (SELECT id FROM t2 LEFT OUTER JOIN t3 ON t2.id = t3.id)"
])
def test_left_join_pass(sql):
    query = Query(sql)
    constraint = LeftJoin()
    constraint.validate(query)

# =================================================================
# TEST LEFT JOIN FAIL
# =================================================================

@pytest.mark.parametrize("sql", [
    "SELECT * FROM t", # no JOIN
    "SELECT * FROM t1 JOIN t2 ON t1.id = t2.id", # INNER JOIN
    "SELECT * FROM t1 RIGHT JOIN t2 ON t1.id = t2.id" # only RIGHT
])
def test_left_join_fail(sql):
    query = Query(sql)
    constraint = LeftJoin()

    with pytest.raises(ConstraintValidationError) as exc_info:
        constraint.validate(query)

# =================================================================
# TEST RIGHT JOIN PASS
# =================================================================

@pytest.mark.parametrize("sql", [
    "SELECT * FROM t1 RIGHT JOIN t2 ON t1.id = t2.id",
    "SELECT * FROM t1 RIGHT OUTER JOIN t2 ON t1.id = t2.id",
    "SELECT * FROM t1 JOIN t2 ON t1.id = t2.id RIGHT JOIN t3 ON t2.id = t3.id",
    "SELECT * FROM t1 WHERE id IN (SELECT id FROM t2 RIGHT OUTER JOIN t3 ON t2.id = t3.id)"
])
def test_right_join_pass(sql):
    query = Query(sql)
    constraint = RightJoin()
    # Deve passare senza sollevare eccezioni
    constraint.validate(query)

# =================================================================
# TEST RIGHT JOIN FAIL
# =================================================================

@pytest.mark.parametrize("sql", [
    "SELECT * FROM t", # No JOIN
    "SELECT * FROM t1 JOIN t2 ON t1.id = t2.id", # INNER JOIN
    "SELECT * FROM t1 LEFT JOIN t2 ON t1.id = t2.id", # Solo LEFT
])
def test_right_join_fail(sql):
    query = Query(sql)
    constraint = RightJoin()
    with pytest.raises(ConstraintValidationError) as exc_info:
        constraint.validate(query)

# =================================================================
# TEST NO JOIN FAIL
# =================================================================

def test_no_join_fail():
    sql_1 = "SELECT * FROM t1 JOIN t2 ON t1.id = t2.id" # JOIN explicit
    sql_2 = "SELECT * FROM t1, t2" # JOIN implicit
    
    for sql in [sql_1, sql_2]:
        query = Query(sql)
        constraint = NoJoin()
        with pytest.raises(ConstraintValidationError):
            constraint.validate(query)

# =================================================================
# TEST NO JOIN PASS
# =================================================================

def test_no_join_pass():
    sql = "SELECT * FROM t1 WHERE id = 10"
    query = Query(sql)
    constraint = NoJoin()
    constraint.validate(query)


# =================================================================
# TEST SELF JOIN FAIL
# =================================================================

def test_self_join_fail():
    sql = "SELECT * FROM t1 JOIN t2 ON t1.id = t2.id"
    query = Query(sql)
    constraint = SelfJoin()
    with pytest.raises(ConstraintValidationError):
        constraint.validate(query)

# =================================================================
# TEST SELF JOIN PASS
# =================================================================

def test_self_join_pass():
    sql = "SELECT e1.name, e2.name FROM t1 e1 JOIN t1 e2 ON e1.id = e2.id"
    query = Query(sql)
    constraint = SelfJoin()
    constraint.validate(query)