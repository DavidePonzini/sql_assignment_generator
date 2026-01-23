'''Constraints related to SQL queries.'''

from .aggregation import RequireAggregation, NoAggregation
from .clause_group_by import RequireGroupBy, NoGroupBy
from .clause_having import RequireHaving, NoHaving
from .from import RequireJoin, NoJoin
from .clause_order_by import RequireOrderBy
from .unique_key import HasUniqueKeyConstraint
from .subquery import HasSubQueryConstraint
from .set_operations import RequireUnion
from .clause_where import HasWhereConstraint
from .rows import RequireDistinct
from .column_number import RequireColumnNumber
from .alias import NoAlias, RequireAlias