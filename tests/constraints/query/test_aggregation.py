import pytest
from sqlscope import Query
from sql_assignment_generator.constraints.query.aggregation import NoAggregation, Aggregation
from sql_assignment_generator.exceptions import ConstraintValidationError


@pytest.mark.parametrize("sql", [
    "SELECT department, COUNT(*) FROM employees GROUP BY department;",
])
def test_no_aggregation_fail(sql):
    query = Query(sql)

    constraint = NoAggregation()

    with pytest.raises(ConstraintValidationError) as exc_info:
        constraint.validate(query)

@pytest.mark.parametrize("sql", [
    "SELECT name, age FROM employees WHERE age > 30;",
])
def test_no_aggregation_pass(sql):
    query = Query(sql)

    constraint = NoAggregation()

    # Should not raise any exception
    constraint.validate(query)

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