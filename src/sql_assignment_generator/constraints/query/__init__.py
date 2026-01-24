'''Constraints related to SQL queries.'''

from .aggregation import RequireAggregation, NoAggregation
from .clause_from import RequireTableReferences, RequireJoin, NoJoin
from .clause_group_by import RequireGroupBy, NoGroupBy
from .clause_having import RequireHaving, NoHaving
from .clause_order_by import RequireOrderBy, RequireOrderByASC, RequireOrderByDESC, NoOrderBy
from .clause_select import RequireColumnNumber, NoAlias, RequireAlias
from .clause_where import HasWhereConstraint
from .rows import RequireDistinct, RequireDuplicates, NoDuplicates, NoDistinct
from .set_operations import RequireUnion, RequireUnionOfType, NoUnion
from .subquery import RequireUnnestedSubqueries, NoSubquery, RequireSubqueries
#from .unique_key import HasUniqueKeyConstraint