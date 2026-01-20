from collections import Counter
from .base import QueryConstraint
from sqlglot import Expression, exp
from ..costraintType import WhereConstraintType, DistinctOrUKInSelectConstraintType, AggregationConstraintType


class HasDistinctOrUniqueKeyInSelectConstraint(QueryConstraint):
    '''
    Checks for uniqueness constraints in the query.
    Can check for the DISTINCT keyword OR for the presence of Key columns in the SELECT clause.

    Args:
        min_tables: Min occurrences required.
        max_tables: Max occurrences required (-1 for no limit).
        state: If True, must be present. If False, must NOT be present.
        type: **DISTINCT**: Checks for DISTINCT keyword. **UK**: Checks for Primary OR Unique Keys in SELECT. **DISTINCT/UK**: Checks for DISTINCT keyword OR Primary/Unique Keys in SELECT.
    '''

    def __init__(self, min_tables: int = 1, max_tables: int = -1, state: bool = True, type: DistinctOrUKInSelectConstraintType = DistinctOrUKInSelectConstraintType.DISTINCT) -> None:
        self.min_tables = min_tables
        self.max_tables = max_tables if max_tables > min_tables else -1
        
        self.state = state
        valid_types = [DistinctOrUKInSelectConstraintType.DISTINCT, DistinctOrUKInSelectConstraintType.UK, DistinctOrUKInSelectConstraintType.DISTINCT_UK]
        if type not in valid_types: raise ValueError(f"type must be one of {valid_types}")
        self.type = type

    def validate(self, query_ast: Expression, tables: list[Expression]) -> bool:
        distinct_count = 0
        key_count = 0

        #DISTINCT case
        if self.type in [DistinctOrUKInSelectConstraintType.DISTINCT, DistinctOrUKInSelectConstraintType.DISTINCT_UK]:
            distinct_nodes = list(query_ast.find_all(exp.Distinct))
            distinct_count = len(distinct_nodes)

        #PK/UK case
        if self.type in [DistinctOrUKInSelectConstraintType.UK, DistinctOrUKInSelectConstraintType.DISTINCT_UK]:
            #identify primary keys and unique keys from tables
            pks = set()
            uks = set()

            for table in tables:
                schema = table.this
                if not isinstance(schema, exp.Schema): continue
                
                #controll all column definitions to find inline PK/UK
                for col_def in schema.find_all(exp.ColumnDef):
                    col_name = col_def.this.output_name.lower()
                    for inline_constraint in col_def.args.get('constraints', []): 
                        if isinstance(inline_constraint.kind, exp.PrimaryKeyColumnConstraint): pks.add(col_name)
                        elif isinstance(inline_constraint.kind, exp.UniqueColumnConstraint): uks.add(col_name)

                #controll definition of Pk/UK at the end of CREATE TABLE (e.g. PRIMARY KEY (col1, col2))
                for constraint in schema.expressions:
                    if isinstance(constraint, exp.PrimaryKey):
                        for col in constraint.expressions:
                            pks.add(col.output_name.lower())
                    elif isinstance(constraint, exp.Constraint):
                        if isinstance(constraint.kind, exp.UniqueColumnConstraint):
                            if constraint.this:
                                cols = constraint.this.expressions if hasattr(constraint.this, 'expressions') else [constraint.this]
                                for col in cols:
                                    if isinstance(col, exp.Column):
                                        uks.add(col.output_name.lower())
                                    elif isinstance(col, exp.Identifier):
                                        uks.add(col.this.lower())

            valid_keys = pks.union(uks) #UK or DISTINCT/UK: accept PK and UK

            #analyze SELECT clause to count how many valid keys are selected
            for select_node in query_ast.find_all(exp.Select):
                for expression in select_node.expressions:
                    found_cols = []
                    if isinstance(expression, exp.Column):
                        found_cols.append(expression.output_name.lower())
                    #case alias controll principal column (es: col AS alias)
                    elif isinstance(expression, exp.Alias):
                        for col in expression.this.find_all(exp.Column):
                            found_cols.append(col.output_name.lower())
                    else:# Case functions or complex expressions(SELECT COUNT(id))
                        for col in expression.find_all(exp.Column):
                            found_cols.append(col.output_name.lower())
                    for col_name in found_cols:
                        if col_name in valid_keys:
                            key_count += 1
                            break
        
        #final count based on type
        if self.type == DistinctOrUKInSelectConstraintType.DISTINCT:
            final_count = distinct_count
        elif self.type == DistinctOrUKInSelectConstraintType.UK:
            final_count = key_count
        else: # DISTINCT/UK - or DISTINCT or KEY
            final_count = distinct_count + key_count

        if not self.state: return final_count == 0
        else: return final_count >= self.min_tables  if self.max_tables < 0 else self.min_tables <= final_count <= self.max_tables
    
    @property
    def description(self) -> str:
        elem_name = self.type.value
        if not self.state: return f"Must NOT have {elem_name}"
        
        if self.max_tables < 0: return f'Must have minimum {self.min_tables} {elem_name}'
        elif self.min_tables == self.max_tables: return f'Must have exactly {self.min_tables} {elem_name}'
        else: return f'Must have between {self.min_tables} and {self.max_tables} {elem_name}'
   