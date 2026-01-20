from collections import Counter
from .base import QueryConstraint
from sqlglot import Expression, exp
from ..costraintType import WhereConstraintType, DistinctOrUKInSelectConstraintType, AggregationConstraintType


class HasAggregationConstraint(QueryConstraint):
    '''Requires the presence (or absence) of an aggregation function in the SQL query. 
    It is possible chose the type of aggregation function present in solution.'''

    def __init__(self, min_tables: int = 1, max_tables: int = -1, type: list[AggregationConstraintType] = [AggregationConstraintType.COUNT], state: bool = True) -> None:
        self.min_tables = min_tables
        self.max_tables = max_tables if max_tables > min_tables else -1

        self.type = type if type is not None else []
        self.state = state

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        type_map = {
            AggregationConstraintType.SUM: exp.Sum,
            AggregationConstraintType.AVG: exp.Avg,
            AggregationConstraintType.COUNT: exp.Count,
            AggregationConstraintType.MAX: exp.Max,
            AggregationConstraintType.MIN: exp.Min,
            AggregationConstraintType.EXTRACT: exp.Extract,
            AggregationConstraintType.LENGTH: exp.Length
        }

        #if type is empty consider all aggregation functions
        if not self.type: target_types = tuple(type_map.values())
        else: #if type has value take only sqlglot needed
            target_types = tuple(
                type_map[t] for t in self.type 
                if t in type_map
            )

            if not target_types:
                target_types = (exp.AggExp)

        # find_all(tuple) find all occurence in query and subquery
        aggregations_found = list(query_ast.find_all(target_types))
        count = len(aggregations_found)

        if not self.state: #case must NOT have AGGREGATION
            return count == 0
        else: #case must have AGGREGATION
            return self.min_tables <= count <= self.max_tables if self.max_tables > 0 else self.min_tables <= count
    
    @property
    def description(self) -> str:
        type_suffix = ""
        if self.type:
            joined_types = " or ".join(t.value.upper() for t in self.type)
            type_suffix = f"of type {joined_types}"
        if self.state == False: return "Must NOT have AGGREGATION"
        if (self.min_tables > self.max_tables): return f'Must have minimum {self.min_tables} AGGREGATION {type_suffix}' 
        elif (self.min_tables == self.max_tables): return f'Must have exactly {self.min_tables} AGGREGATION {type_suffix}'
        else: return f'Must have between {self.min_tables} and {self.max_tables} AGGREGATION {type_suffix}'
