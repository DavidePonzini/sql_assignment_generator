import pytest
from sqlscope import Query
from sql_assignment_generator.constraints.query.aggregation import NoAggregation, NoPartitioning, Aggregation
from sql_assignment_generator.exceptions import ConstraintValidationError

# =================================================================
# TEST NO PARTITIONING FAIL
# =================================================================

@pytest.mark.parametrize("sql", [
    "SELECT ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary) AS rn FROM employees;",
    "SELECT name FROM employees WHERE salary > (SELECT AVG(salary) OVER (PARTITION BY department) FROM employees LIMIT 1);",
    "SELECT name FROM employees ORDER BY ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary);",
])
def test_no_partitioning_fail(sql):
    query = Query(sql)
    constraint = NoPartitioning()

    with pytest.raises(ConstraintValidationError):
        constraint.validate(query)


# =================================================================
# TEST NO PARTITIONING PASS
# =================================================================

@pytest.mark.parametrize("sql", [
    "SELECT name, salary + bonus AS total_compensation FROM employees;",
    "SELECT department, AVG(salary) FROM employees GROUP BY department;",
    "SELECT name FROM employees WHERE salary > 50000 ORDER BY salary DESC;",
])
def test_no_partitioning_pass(sql):
    query = Query(sql)
    constraint = NoPartitioning()

    constraint.validate(query)


# =================================================================
# TEST NO AGGREGATION FAIL
# =================================================================

def test_no_aggregation_fail():
    sql = "SELECT department, COUNT(*) FROM employees GROUP BY department;"
    query = Query(sql)

    constraint = NoAggregation()

    with pytest.raises(ConstraintValidationError) as exc_info:
        constraint.validate(query)

# =================================================================
# TEST NO AGGREGATION PASS
# =================================================================

def test_no_aggregation_pass():
    sql = "SELECT name, age FROM employees WHERE age > 30;"
    query = Query(sql)

    constraint = NoAggregation()

    # Should not raise any exception
    constraint.validate(query)

# =================================================================
# TEST AGGREGATION FAIL
# =================================================================
@pytest.mark.parametrize("sql,min_,max_,allowed_functions", [
    ("SELECT name, age FROM employees WHERE age > 30;", 1, None, ['AVG', 'SUM', 'COUNT', 'MIN', 'MAX']),
    ("SELECT department, SUM(salary) FROM employees GROUP BY department;", 2, None, ['AVG', 'SUM', 'COUNT', 'MIN', 'MAX']),
    ("SELECT department, SUM(salary), COUNT(*) FROM employees GROUP BY department;", 1, 1, ['AVG', 'SUM', 'COUNT', 'MIN', 'MAX']),
    ("SELECT department, AVG(salary), MAX(age) FROM employees GROUP BY department;", 2, None, ['AVG', 'SUM']),
    ("SELECT department, AVG(salary), MAX(age), COUNT(*) FROM employees GROUP BY department;", 1, 2, ['AVG', 'MAX', 'COUNT']),
])

def test_aggregation_fail(sql, min_, max_, allowed_functions):
    query = Query(sql)

    constraint = Aggregation(min_=min_, max_=max_, allowed_functions=allowed_functions)

    with pytest.raises(ConstraintValidationError) as exc_info:
        constraint.validate(query)

# =================================================================
# TEST AGGREGATION PASS
# =================================================================
@pytest.mark.parametrize("sql,min_,max_,allowed_functions", [
    ("SELECT department, SUM(salary) FROM employees GROUP BY department;", 1, None, ['AVG', 'SUM', 'COUNT', 'MIN', 'MAX']),
    ("SELECT department, AVG(salary), MAX(age) FROM employees GROUP BY department;", 2, None, ['AVG', 'SUM', 'COUNT', 'MIN', 'MAX']),
    ("SELECT department, SUM(salary), COUNT(*) FROM employees GROUP BY department;", 1, 2, ['AVG', 'SUM', 'COUNT', 'MIN', 'MAX']),
    ("SELECT department, AVG(salary), MAX(age), COUNT(*) FROM employees GROUP BY department;", 3, 3, ['AVG', 'MAX', 'COUNT']),
    ("SELECT department, AVG(salary), MAX(age), COUNT(*) FROM employees GROUP BY department;", 2, 2, ['AVG', 'MAX']),
])

def test_aggregation_pass(sql, min_, max_, allowed_functions):
    query = Query(sql)

    constraint = Aggregation(min_=min_, max_=max_, allowed_functions=allowed_functions)
    
    # Should not raise any exception
    constraint.validate(query)
