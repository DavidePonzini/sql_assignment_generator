'''Constraints related to database schema.'''

from collections.abc import Sequence
from .base import SchemaConstraint
from . import tables, values


def merge_constraints(constraints: Sequence[SchemaConstraint]) -> Sequence[SchemaConstraint]:
    '''Merge similar schema constraints into a single set of constraints.'''
    merged_constraints_map = {}
    
    for constraint in constraints:
        c_type = constraint.__class__.__name__

        # if constraint type already exists, we can merge them
        if c_type in merged_constraints_map:
            existing_constraint = merged_constraints_map[c_type]
            merged_constraint = existing_constraint.merge(constraint)
            merged_constraints_map[c_type] = merged_constraint
        else:
            merged_constraints_map[c_type] = constraint

    return list(merged_constraints_map.values())

