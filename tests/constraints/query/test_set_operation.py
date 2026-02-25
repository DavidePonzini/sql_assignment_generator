import pytest
from sqlscope import Query
from sql_assignment_generator.constraints.query.set_operations import (
    Union, 
    NoUnion, 
    UnionOfType
)
from sql_assignment_generator.exceptions import ConstraintValidationError

# =================================================================
# TEST UNION PASS
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT * FROM t1 UNION SELECT * FROM t2", 1, None), # 1 UNION, min 1 required
    ("SELECT * FROM t1 UNION ALL SELECT * FROM t2", 1, None), # 1 UNION ALL, min 1 required
    ("SELECT * FROM t1 UNION SELECT * FROM t2 UNION ALL SELECT * FROM t3", 2, 2), # exactly 2 operations
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2 UNION SELECT id FROM t3)", 1, 1), # 1 UNION inside subquery
    ("SELECT * FROM (SELECT * FROM t1) AS sub1 UNION ALL SELECT * FROM (SELECT * FROM t2) AS sub2;", 1, None) # UNION ALL with FROM subquery
])
def test_union_pass(sql, min_, max_):
    query = Query(sql)
    constraint = Union(min_=min_, max_=max_)
    constraint.validate(query)


# =================================================================
# TEST UNION FAIL
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT * FROM t1", 1, None), # 0 operations found, but 1 required
    ("SELECT * FROM t1 UNION SELECT * FROM t2", 2, None), # 1 found, but 2 required
    ("SELECT * FROM t1 UNION SELECT * FROM t2 UNION SELECT * FROM t3", 1, 1), # 2 found, but max 1 allowed
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2)", 1, None) # 0 operations in query with subquery
])
def test_union_fail(sql, min_, max_):
    query = Query(sql)
    constraint = Union(min_=min_, max_=max_)
    with pytest.raises(ConstraintValidationError):
        constraint.validate(query)


# =================================================================
# TEST NO UNION PASS
# =================================================================

@pytest.mark.parametrize("sql", [
    "SELECT * FROM t1",
    "SELECT * FROM t1 JOIN t2 ON t1.id = t2.id",
    "SELECT * FROM t1 WHERE id IN (SELECT id FROM t2)" # Subquery without UNION is fine
])
def test_no_union_pass(sql):
    query = Query(sql)
    constraint = NoUnion()
    constraint.validate(query)


# =================================================================
# TEST NO UNION FAIL
# =================================================================

@pytest.mark.parametrize("sql", [
    "SELECT * FROM t1 UNION SELECT * FROM t2",
    "SELECT * FROM t1 UNION ALL SELECT * FROM t2",
    "SELECT * FROM t1 WHERE id IN (SELECT id FROM t2 UNION SELECT id FROM t3)"
])
def test_no_union_fail(sql):
    query = Query(sql)
    constraint = NoUnion()
    with pytest.raises(ConstraintValidationError):
        constraint.validate(query)


# =================================================================
# TEST UNION OF TYPE PASS
# =================================================================

@pytest.mark.parametrize("sql, is_all, min_, max_", [
    ("SELECT * FROM t1 UNION SELECT * FROM t2", False, 1, None), # 1 UNION (distinct), min 1
    ("SELECT * FROM t1 UNION ALL SELECT * FROM t2", True, 1, None), # 1 UNION ALL, min 1
    ("SELECT DISTINCT * FROM t1 UNION ALL SELECT * FROM t2 UNION SELECT * FROM t3", False, 1, 1), # 1 UNION (distinct) exists
    ("SELECT * FROM t1 UNION ALL SELECT * FROM t2 UNION ALL SELECT * FROM t3", True, 2, 2), # 2 UNION ALL exist
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2 UNION ALL SELECT id FROM t3)", True, 1, 1), # 1 UNION ALL in subquery
    ("SELECT * FROM (SELECT * FROM t1) AS sub1 UNION SELECT * FROM (SELECT * FROM t2) AS sub2", False, 1, 1) # 1 UNION out of subquery
])
def test_union_of_type_pass(sql, is_all, min_, max_):
    query = Query(sql)
    constraint = UnionOfType(all=is_all, min_=min_, max_=max_)
    constraint.validate(query)


# =================================================================
# TEST UNION OF TYPE FAIL
# =================================================================

@pytest.mark.parametrize("sql, is_all, min_, max_", [
    ("SELECT * FROM t1 UNION SELECT * FROM t2", True, 1, None), # Looking for UNION ALL, but found UNION (distinct)
    ("SELECT * FROM t1 UNION ALL SELECT * FROM t2", False, 1, None), # Looking for UNION (distinct), but found UNION ALL
    ("SELECT * FROM t1 UNION SELECT * FROM t2 UNION ALL SELECT * FROM t3", True, 2, None), # Found 1 UNION ALL, but 2 required
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2 UNION SELECT id FROM t3)", True, 1, None), # Looking for ALL in subquery, found Distinct
    ("SELECT * FROM (SELECT * FROM t1) AS sub1 UNION ALL SELECT * FROM (SELECT * FROM t2) AS sub2", False, 1, 1) # 1 wrong UNION out of subquery
])
def test_union_of_type_fail(sql, is_all, min_, max_):
    query = Query(sql)
    constraint = UnionOfType(all=is_all, min_=min_, max_=max_)
    with pytest.raises(ConstraintValidationError):
        constraint.validate(query)