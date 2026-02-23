import pytest
from sqlscope import Query
from sql_assignment_generator.constraints.query.clause_where import (
    Condition, 
    StringComparison, 
    EmptyStringComparison, 
    NullComparison, 
    NotNullComparison, 
    NoLike, 
    Not, 
    Exists, 
    NotExist, 
    MathOperators, 
    WildcardCharacters, 
    WildcardLength, 
    Condition_WhereHaving, 
    MultipleConditionsOnSameColumn,
    InAnyAll
)
from sql_assignment_generator.exceptions import ConstraintValidationError

# =================================================================
# TEST CONDITION PASS
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT * FROM t1 WHERE a = 1 AND b = 'anything'", 2, None),
    ("SELECT * FROM t1 WHERE a = 1 AND b = 2 AND c = 3", 2, 3),
    ("SELECT * FROM t1 WHERE (a = 1 OR b = 2) AND c = 3", 3, None),
    ("SELECT * FROM t1 WHERE a = 1 UNION SELECT * FROM t1 WHERE b = 2", 2, None),
    ("SELECT * FROM t1 WHERE a BETWEEN 1 AND 10 OR b IN (1, 2, 3)", 2, None),
    ("SELECT * FROM t1 WHERE a LIKE '%something'", 1, None),
    ("SELECT * FROM t1 WHERE a IS NULL", 1, None),
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2 WHERE a = 'something') AND b > 500;", 1, 3),
    ("SELECT a FROM t1 p WHERE EXISTS (SELECT 1 FROM t2 s WHERE s.id = p.id AND s.b > 100);", 1, 3),
    ("SELECT * FROM t1 WHERE NOT EXISTS (SELECT 1 FROM t2 WHERE t2.id = t1.id)", 2, 2),
])

def test_condition_pass(sql, min_, max_):
    query = Query(sql)
    constraint = Condition(min_=min_, max_=max_)
    constraint.validate(query)


# =================================================================
# TEST CONDITION FAIL
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT * FROM t1", 1, None),
    ("SELECT * FROM t1 WHERE a = 1", 2, None),
    ("SELECT * FROM t1 WHERE a = 1 AND b = 2 AND c = 3", 1, 2),
    ("SELECT * FROM t1 WHERE a = 1 OR b = 2", 3, 3),
    ("SELECT * FROM t1 p WHERE EXISTS (SELECT 1 FROM t2 s WHERE s.id = p.id AND s.a > 100);", 1, 2),
])

def test_condition_fail(sql, min_, max_):
    query = Query(sql)
    constraint = Condition(min_=min_, max_=max_)
    with pytest.raises(ConstraintValidationError) as exc_info:
        constraint.validate(query)

# =================================================================
# TEST STRING COMPARISON PASS
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT * FROM t WHERE a = 'Alice'", 1, None),
    ("SELECT * FROM t WHERE 'Rome' = a", 1, None),
    ("SELECT * FROM t WHERE a = 'Something' AND b LIKE '%Something'", 2, None),
    ("SELECT * FROM t WHERE a = 'Something' AND b > 18", 1, 1),
    ("SELECT * FROM t WHERE a <> 'Something'", 1, None),
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2 WHERE a = 'Something');", 1, None),
    ("SELECT * FROM t1 WHERE a = 'Something' AND id IN (SELECT id FROM t2 WHERE a = 'Something');", 1, 2)
])
def test_string_comparison_pass(sql, min_, max_):
    query = Query(sql)
    constraint = StringComparison(min_=min_, max_=max_)
    constraint.validate(query)


# =================================================================
# TEST STRING COMPARISON FAIL
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT * FROM t", 1, None),
    ("SELECT * FROM t WHERE a = 20 AND b = c", 1, None),
    ("SELECT * FROM t WHERE 'abc' = 'abc'", 1, None),
    ("SELECT * FROM t WHERE a = 'SomeThing' AND p > 10", 2, None),
    ("SELECT * FROM t WHERE a = 'SomeThing1' OR a = 'SomeThing2'", 0, 1),
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2 WHERE a = 3);", 1, None),
])
def test_string_comparison_fail(sql, min_, max_):
    query = Query(sql)
    constraint = StringComparison(min_=min_, max_=max_)
    with pytest.raises(ConstraintValidationError) as exc_info:
        constraint.validate(query)

# =================================================================
# TEST EMPTY STRING COMPARISON PASS
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT * FROM t WHERE a = '' AND b <> ''", 2, None),
    ("SELECT * FROM t WHERE '' = a", 1, None),
    ("SELECT * FROM t WHERE a = '' OR b <> ''", 2, None),
    ("SELECT * FROM t WHERE a = '' AND b = 'Something' AND c > 18", 1, 1),
    ("SELECT * FROM t1 WHERE id NOT IN (SELECT id FROM t2 WHERE a <> '');", 1, None),
    ("SELECT a FROM t1 WHERE id IN (SELECT id FROM t2 WHERE b = '') AND c = '';", 2, 2),
])

def test_empty_string_comparison_pass(sql, min_, max_):
    query = Query(sql)
    constraint = EmptyStringComparison(min_=min_, max_=max_)
    constraint.validate(query)

# =================================================================
# TEST EMPTY STRING COMPARISON FAIL
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT * FROM t WHERE a = ' '", 1, None), # space is no empty
    ("SELECT * FROM t WHERE a = 'N/A'", 1, None),
    ("SELECT * FROM t WHERE a IS NULL", 1, None),
    ("SELECT * FROM t WHERE a LIKE ''", 1, None), # like is no empty case
    ("SELECT * FROM t WHERE '' = ''", 1, None),
    ("SELECT * FROM t WHERE a = ''", 2, None),
    ("SELECT * FROM t WHERE a = '' OR b = ''", 0, 1),
    ("SELECT a FROM t1 WHERE id IN (SELECT id FROM t2 WHERE b = '') AND c = 2;", 2, None),
])

def test_empty_string_comparison_fail(sql, min_, max_):
    query = Query(sql)
    constraint = EmptyStringComparison(min_=min_, max_=max_)
    with pytest.raises(ConstraintValidationError) as exc_info:
        constraint.validate(query)

# =================================================================
# TEST NULL COMPARISON PASS
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT * FROM t WHERE a IS NULL", 1, None),
    ("SELECT * FROM t WHERE a IS NULL OR b IS NULL AND c = 2", 1, 2),
    ("SELECT * FROM t WHERE a IS NULL AND b IS NOT NULL", 1, 1),
    ("SELECT * FROM t1 WHERE a IS NULL AND id IN (SELECT id FROM t2 WHERE b IS NULL)", 2, None),
    ("SELECT * FROM t1 p WHERE p.x IS NULL AND EXISTS (SELECT 1 FROM t2 s WHERE s.id = p.id AND s.y IS NULL)", 2, 2),
])

def test_null_comparison_pass(sql, min_, max_):
    query = Query(sql)
    constraint = NullComparison(min_=min_, max_=max_)
    constraint.validate(query)

# =================================================================
# TEST NULL COMPARISON FAIL
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT * FROM t", 1, None),
    ("SELECT * FROM t WHERE a = 'active'", 1, None),
    ("SELECT * FROM t WHERE a IS NOT NULL", 1, None),
    ("SELECT * FROM t WHERE a IS NULL AND b = 5", 2, None),
    ("SELECT * FROM t WHERE a IS NULL OR b IS NULL", 0, 1),
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2 WHERE b IS NOT NULL)", 1, None)
])

def test_null_comparison_fail(sql, min_, max_):
    query = Query(sql)
    constraint = NullComparison(min_=min_, max_=max_)
    with pytest.raises(ConstraintValidationError) as exc_info:
        constraint.validate(query)

# =================================================================
# TEST NOT NULL COMPARISON PASS
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT * FROM t WHERE a IS NOT NULL", 1, None),
    ("SELECT * FROM t WHERE a IS NOT NULL AND b = 3", 1, 1),
    ("SELECT * FROM t WHERE a IS NOT NULL AND b IS NULL", 1, 1),
    ("SELECT * FROM t1 WHERE a IS NOT NULL AND id IN (SELECT id FROM t2 WHERE b IS NOT NULL)", 2, None),
    ("SELECT * FROM t1 s WHERE s.a IS NOT NULL AND EXISTS (SELECT 1 FROM t2 e WHERE e.id = s.id AND e.b IS NOT NULL)", 2, 2)
])

def test_not_null_comparison_pass(sql, min_, max_):
    query = Query(sql)
    constraint = NotNullComparison(min_=min_, max_=max_)
    constraint.validate(query)


# =================================================================
# TEST NOT NULL COMPARISON FAIL
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT * FROM t", 1, None),
    ("SELECT * FROM t WHERE a = 'something'", 1, None),
    ("SELECT * FROM t WHERE a IS NULL", 1, None),
    ("SELECT * FROM t WHERE a IS NOT NULL AND b = 5", 2, None),
    ("SELECT * FROM t WHERE a IS NOT NULL OR b IS NOT NULL", 0, 1),
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2 WHERE b IS NULL)", 1, None)
])

def test_not_null_comparison_fail(sql, min_, max_):
    query = Query(sql)
    constraint = NotNullComparison(min_=min_, max_=max_)
    with pytest.raises(ConstraintValidationError) as exc_info:
        constraint.validate(query)

# =================================================================
# TEST NO LIKE PASS
# =================================================================

@pytest.mark.parametrize("sql", [
    "SELECT * FROM t",
    "SELECT * FROM t WHERE a = 'something'",
    "SELECT * FROM t WHERE a > 100 AND b >= 'something'",
    "SELECT * FROM t WHERE a IS NOT NULL",
    "SELECT * FROM t1 WHERE id IN (SELECT id FROM t2 WHERE a = 'something')",
    "SELECT * FROM t1 WHERE a = '100%'", #percentage but without like
])

def test_no_like_pass(sql):
    query = Query(sql)
    constraint = NoLike()
    constraint.validate(query)


# =================================================================
# TEST NO LIKE FAIL
# =================================================================

@pytest.mark.parametrize("sql", [
    "SELECT * FROM t WHERE a LIKE 'A%'",
    "SELECT * FROM t WHERE a ILIKE 'something%'",
    "SELECT * FROM t WHERE (a = 'something' AND b LIKE '%something%') OR c < 10",
    "SELECT * FROM t1 WHERE id IN (SELECT id FROM t2 WHERE a LIKE '%something%')",
    "SELECT * FROM t WHERE email NOT LIKE '%something'",
])

def test_no_like_fail(sql):
    query = Query(sql)
    constraint = NoLike()
    with pytest.raises(ConstraintValidationError) as exc_info:
        constraint.validate(query)

# =================================================================
# TEST NOT PASS
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT * FROM t WHERE NOT (a = 'something')", 1, None),
    ("SELECT * FROM t WHERE id NOT IN (1, 2, 3)", 1, None),
    ("SELECT * FROM t WHERE a NOT LIKE 'A%'", 1, None),
    ("SELECT * FROM t WHERE a IS NOT NULL", 1, None),
    ("SELECT * FROM t1 WHERE NOT EXISTS (SELECT 1 FROM t2 WHERE t1.id = t2.id)", 1, None),
    ("SELECT * FROM t WHERE NOT a = 1 AND b NOT IN (10, 20)", 2, 2),
    ("SELECT * FROM t1 WHERE NOT a = 1 AND id IN (SELECT id FROM t2 WHERE b NOT LIKE 'x%')", 2, 2)
])

def test_not_pass(sql, min_, max_):
    query = Query(sql)
    constraint = Not(min_=min_, max_=max_)
    constraint.validate(query)


# =================================================================
# TEST NOT FAIL
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT * FROM t", 1, None),
    ("SELECT * FROM t WHERE a = 1", 1, None),
    ("SELECT * FROM t WHERE NOT a = 1 AND b = 2", 2, None),
    ("SELECT * FROM t WHERE a NOT IN (1, 2) OR b IS NOT NULL", 0, 1),
    ("SELECT * FROM t1 WHERE a = 1 AND id IN (SELECT id FROM t2 WHERE b LIKE 'x%')", 1, None)
])

def test_not_fail(sql, min_, max_):
    query = Query(sql)
    constraint = Not(min_=min_, max_=max_)
    with pytest.raises(ConstraintValidationError) as exc_info:
        constraint.validate(query)

# =================================================================
# TEST EXISTS PASS
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT * FROM t1 WHERE EXISTS (SELECT 1 FROM t2 WHERE t2.id = t1.id)", 1, None),
    ("SELECT * FROM t1 WHERE EXISTS (SELECT 1 FROM t2) AND EXISTS (SELECT 1 FROM t3)", 2, None),
    ("SELECT * FROM t1 WHERE EXISTS (SELECT 1 FROM t2) AND NOT EXISTS (SELECT 1 FROM t3)", 1, 1),
    ("SELECT * FROM t1 WHERE EXISTS (SELECT 1 FROM t2 WHERE EXISTS (SELECT 1 FROM t3))", 2, 2),
    ("SELECT * FROM t1 WHERE EXISTS (SELECT 1 FROM t2) OR a = 3", 1, 2),
])

def test_exists_pass(sql, min_, max_):
    query = Query(sql)
    constraint = Exists(min_=min_, max_=max_)
    constraint.validate(query)


# =================================================================
# TEST EXISTS FAIL
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT * FROM t1", 1, None),
    ("SELECT * FROM t1 WHERE a = 1", 1, None),
    ("SELECT * FROM t1 WHERE NOT EXISTS (SELECT 1 FROM t2)", 1, None),
    ("SELECT * FROM t1 WHERE EXISTS (SELECT 1 FROM t2) AND a = 1", 2, None),
    ("SELECT * FROM t1 WHERE EXISTS (SELECT 1 FROM t2) AND EXISTS (SELECT 1 FROM t3)", 0, 1),
])

def test_exists_fail(sql, min_, max_):
    query = Query(sql)
    constraint = Exists(min_=min_, max_=max_)
    with pytest.raises(ConstraintValidationError) as exc_info:
        constraint.validate(query)

# =================================================================
# TEST NOT EXIST PASS
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT * FROM t1 WHERE NOT EXISTS (SELECT 1 FROM t2 WHERE t2.id = t1.id)", 1, None),
    ("SELECT * FROM t1 WHERE NOT EXISTS (SELECT 1 FROM t2) AND NOT EXISTS (SELECT 1 FROM t3)", 2, 2),
    ("SELECT * FROM t1 WHERE EXISTS (SELECT 1 FROM t2) AND NOT EXISTS (SELECT 1 FROM t3)", 1, 1),
    ("SELECT * FROM t1 WHERE NOT EXISTS (SELECT 1 FROM t2 WHERE NOT EXISTS (SELECT 1 FROM t3))", 2, 2),
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2 WHERE NOT EXISTS (SELECT 1 FROM t3))", 1, 1),
])

def test_not_exist_pass(sql, min_, max_):
    query = Query(sql)
    constraint = NotExist(min_=min_, max_=max_)
    constraint.validate(query)


# =================================================================
# TEST NOT EXIST FAIL
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT * FROM t1", 1, None),    
    ("SELECT * FROM t1 WHERE a = 1", 1, None),
    ("SELECT * FROM t1 WHERE EXISTS (SELECT 1 FROM t2)", 1, None),
    ("SELECT * FROM t1 WHERE NOT EXISTS (SELECT 1 FROM t2) AND a = 1", 2, None),
    ("SELECT * FROM t1 WHERE NOT EXISTS (SELECT 1 FROM t2 WHERE NOT EXISTS (SELECT 1 FROM t3))", 0, 1),
])

def test_not_exist_fail(sql, min_, max_):
    query = Query(sql)
    constraint = NotExist(min_=min_, max_=max_)
    with pytest.raises(ConstraintValidationError) as exc_info:
        constraint.validate(query)

# =================================================================
# TEST MATH OPERATORS PASS
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT * FROM t WHERE a + b > 100", 1, None),
    ("SELECT * FROM t WHERE a - b > 0", 1, None),
    ("SELECT * FROM t WHERE (a * 12) / 2 > 20000", 2, None),
    ("SELECT * FROM t WHERE id % 2 = 0", 1, None),
    ("SELECT * FROM t WHERE (a + b) * (c - d) > 0", 3, 3),
    ("SELECT * FROM t1 WHERE a + b > (SELECT AVG(c) FROM t2 WHERE d - e > 0)", 2, 2),
    ("SELECT price * 1.22 FROM t WHERE a - b > 50", 1, 1),
])

def test_math_operators_pass(sql, min_, max_):
    query = Query(sql)
    constraint = MathOperators(min_=min_, max_=max_)
    constraint.validate(query)

# =================================================================
# TEST MATH OPERATORS FAIL
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT * FROM t", 1, None),
    ("SELECT * FROM t WHERE a = 10", 1, None),
    ("SELECT * FROM t WHERE a + b > 10", 2, None),
    ("SELECT * FROM t WHERE a * b > 0 AND c / d < 10", 0, 1),
    ("SELECT a + b FROM t WHERE c = 10", 1, None),
    ("SELECT * FROM t1 WHERE a + b > (SELECT x FROM t2 WHERE y * z > 0)", 0, 1),
])

def test_math_operators_fail(sql, min_, max_):
    query = Query(sql)
    constraint = MathOperators(min_=min_, max_=max_)
    with pytest.raises(ConstraintValidationError) as exc_info:
        constraint.validate(query)

# =================================================================
# TEST WILDCARD CHARACTERS PASS
# =================================================================

@pytest.mark.parametrize("sql, req_chars, min_val", [
    ("SELECT * FROM t WHERE name LIKE 'A%'", "%", 1), # (%)
    ("SELECT * FROM t WHERE name LIKE 'A%_'", "%_", 1), # (% e _)
    ("SELECT * FROM t WHERE code LIKE 'ID___'", "__", 1), # (2 '_')
    ("SELECT * FROM t WHERE a LIKE '%x%' AND b LIKE '%y%'", "%", 2), # (min 2 %)
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2 WHERE note LIKE 'test%')", "%", 1), # subquery
    ("SELECT * FROM t WHERE name ILIKE '%alice%'", "%", 1),
    ("SELECT * FROM t WHERE a LIKE '[0-9]%'", "[]", 1),
])

def test_wildcard_characters_pass(sql, req_chars, min_val):
    query = Query(sql)
    constraint = WildcardCharacters(required_characters=req_chars, min_=min_val)
    constraint.validate(query)

# =================================================================
# TEST WILDCARD CHARACTERS FAIL
# =================================================================

@pytest.mark.parametrize("sql, req_chars, min_val", [
    ("SELECT * FROM t", "%", 1),
    ("SELECT * FROM t WHERE a = 10", "%", 1),
    ("SELECT * FROM t WHERE name LIKE 'A%'", "_", 1), # (miss '_')
    ("SELECT * FROM t WHERE name LIKE 'A%'", "%%", 1), # (need min 2 '%')
    ("SELECT * FROM t WHERE a LIKE '%a%' AND b LIKE 'abc'", "%", 2),
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2 WHERE a LIKE 'something')", "%", 1),
])

def test_wildcard_characters_fail(sql, req_chars, min_val):
    query = Query(sql)
    constraint = WildcardCharacters(required_characters=req_chars, min_=min_val)
    with pytest.raises(ConstraintValidationError) as exc_info:
        constraint.validate(query)

# =================================================================
# TEST WILDCARD LENGTH PASS
# =================================================================

@pytest.mark.parametrize("sql, min_val, max_val", [
    ("SELECT * FROM t WHERE a LIKE 'User%'", 4, None),
    ("SELECT * FROM t WHERE a ILIKE '%aaaa%'", 4, 6),
    ("SELECT * FROM t WHERE a LIKE 'aaa_'", 3, 3),
    ("SELECT * FROM t WHERE a LIKE 'aaaa/%/_'", 4, None),
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2 WHERE a LIKE '%aaaa%')", 4, None),
    ("SELECT * FROM t WHERE a LIKE 'LongName%' AND b LIKE 'OtherName%'", 5, None),
])

def test_wildcard_length_pass(sql, min_val, max_val):
    query = Query(sql)
    constraint = WildcardLength(min_=min_val, max_=max_val)
    constraint.validate(query)

# =================================================================
# TEST WILDCARD LENGTH FAIL
# =================================================================

@pytest.mark.parametrize("sql, min_val, max_val", [
    ("SELECT * FROM t WHERE a LIKE 'Ab%'", 4, None),
    ("SELECT * FROM t WHERE a LIKE '%ABCDEFG%'", 1, 5),
    ("SELECT * FROM t WHERE a LIKE 'Admin'", 1, None),
    ("SELECT * FROM t WHERE a = 10", 1, None),
    ("SELECT a LIKE 'A%' as check FROM t", 1, None),
    ("SELECT * FROM t WHERE a LIKE 'ValidName%' AND b LIKE 'No%'", 4, None),
])

def test_wildcard_length_fail(sql, min_val, max_val):
    query = Query(sql)
    constraint = WildcardLength(min_=min_val, max_=max_val)
    with pytest.raises(ConstraintValidationError):
        constraint.validate(query)

# =================================================================
# TEST WHERE_HAVING PASS
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT * FROM t WHERE a = 1 AND b = 2", 2, None),
    ("SELECT a FROM t GROUP BY a HAVING SUM(b) > 100 OR AVG(b) < 10", 2, None),
    ("SELECT * FROM t WHERE a=1 AND b=2 OR c=3", 2, None),
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2 WHERE x=1 AND y=2)", 2, 2),
    ("SELECT * FROM t1 HAVING SUM(a) > (SELECT SUM(b) FROM t2 HAVING count(*) > 1)", 1, 1),
    ("SELECT * FROM t1 WHERE a=1 OR b=2 UNION SELECT * FROM t1 WHERE c=3", 2, None),
])

def test_where_having_pass(sql, min_, max_):
    query = Query(sql)
    constraint = Condition_WhereHaving(min_=min_, max_=max_)
    constraint.validate(query)


# =================================================================
# TEST WHERE_HAVING FAIL
# =================================================================

@pytest.mark.parametrize("sql, min_, max_", [
    ("SELECT a FROM t WHERE b > 0 GROUP BY a HAVING COUNT(*) > 5", 2, None), 
    ("SELECT a FROM t WHERE b > 0 GROUP BY a HAVING COUNT(*) > 5", 1, None),
    ("SELECT * FROM t WHERE a = 1 AND b = 2", 1, 1),
    ("SELECT * FROM t", 1, None),
    ("SELECT * FROM t WHERE a=1 UNION SELECT * FROM t WHERE b=2", 2, None),
    ("SELECT * FROM t1 WHERE a=1 AND id IN (SELECT id FROM t2 WHERE b=2)", 3, None),
])

def test_where_having_fail(sql, min_, max_):
    query = Query(sql)
    constraint = Condition_WhereHaving(min_=min_, max_=max_)
    with pytest.raises(ConstraintValidationError) as exc_info:
        constraint.validate(query)

# =================================================================
# TEST MULTIPLE CONDITIONS PASS
# =================================================================

@pytest.mark.parametrize("sql, min_cols", [
    ("SELECT * FROM t WHERE age > 18 AND age < 30", 1),
    ("SELECT * FROM t WHERE A = 'something' OR A <> 'anything'", 1),
    ("SELECT * FROM t WHERE price BETWEEN 10 AND 100 AND price <> 50", 1),
    ("SELECT * FROM t WHERE a > 1 AND a < 10 AND b = 'X' OR b = 'Y'", 2),
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2 WHERE x = 1 OR x = 2)", 1),
    ("SELECT * FROM t WHERE a = 1 OR a = 2 AND b = 3 AND c = 4", 1),
])

def test_multiple_conditions_pass(sql, min_cols):
    query = Query(sql)
    constraint = MultipleConditionsOnSameColumn(min_columns=min_cols)
    constraint.validate(query)

# =================================================================
# TEST MULTIPLE CONDITIONS FAIL
# =================================================================

@pytest.mark.parametrize("sql, min_cols", [
    ("SELECT * FROM t WHERE a = 1 AND b = 2", 1),
    ("SELECT * FROM t WHERE age > 18", 1),
    ("SELECT * FROM t WHERE a = 1 OR a = 2 AND b = 3", 2),
    ("SELECT * FROM t", 1),
    ("SELECT * FROM t1 WHERE a = 1 AND id IN (SELECT id FROM t1 WHERE a = 2)", 1),
])

def test_multiple_conditions_fail(sql, min_cols):
    query = Query(sql)
    constraint = MultipleConditionsOnSameColumn(min_columns=min_cols)
    with pytest.raises(ConstraintValidationError) as exc_info:
        constraint.validate(query)

# =================================================================
# TEST IN_ANY_ALL PASS
# =================================================================

@pytest.mark.parametrize("sql, min_val", [
    ("SELECT * FROM t WHERE id IN (1, 2, 3)", 1),
    ("SELECT * FROM t WHERE id IN (SELECT id FROM t2)", 1),
    ("SELECT * FROM t WHERE a > ANY (SELECT b FROM t2)", 1),
    ("SELECT * FROM t WHERE a >= ALL (SELECT b FROM t2)", 1),
    ("SELECT * FROM t WHERE a IN (1,2) AND b IN (SELECT x FROM t2)", 2),
    ("SELECT * FROM t WHERE id IN (1,2) OR price < ALL (SELECT p FROM t2)", 2),
    ("SELECT * FROM t1 WHERE id IN (SELECT x FROM t2 WHERE val > ANY (SELECT y FROM t3))", 2),
    ("SELECT * FROM t1 WHERE id IN (SELECT id FROM t2 WHERE a > ANY (SELECT b FROM t3 WHERE c = ALL (SELECT d FROM t4)))", 3)
])

def test_in_any_all_pass(sql, min_val):
    query = Query(sql)
    constraint = InAnyAll(min_=min_val)
    constraint.validate(query)

# =================================================================
# TEST IN_ANY_ALL FAIL
# =================================================================

@pytest.mark.parametrize("sql, min_val", [
    ("SELECT * FROM t", 1),
    ("SELECT * FROM t WHERE id = 10", 1),
    ("SELECT * FROM t WHERE id IN (1, 2)", 2),
    ("SELECT * FROM t1 WHERE EXISTS (SELECT 1 FROM t2 WHERE t1.id = t2.id)", 1),
    ("SELECT * FROM t WHERE name LIKE 'A%' AND price > 100", 1),
])

def test_in_any_all_fail(sql, min_val):
    query = Query(sql)
    constraint = InAnyAll(min_=min_val)
    with pytest.raises(ConstraintValidationError) as exc_info:
        constraint.validate(query)