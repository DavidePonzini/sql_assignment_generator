import sqlglot
from sqlglot import expressions as exp
from sqlscope import build_catalog_from_sql, Catalog, Dialect

def prepare_catalog(create_sqls: list[str] = [], insert_sqls: list[str] = []) -> tuple[Catalog, list[exp.Create], list[exp.Insert]]:
    '''Helper function to prepare the environment for validation'''

    table_asts: list[exp.Create] = []
    for sql in create_sqls:
        ast = sqlglot.parse_one(sql, dialect=Dialect.POSTGRES.get_sqlglot_dialect())
        if not isinstance(ast, exp.Create):
            raise ValueError(f"Expected CREATE TABLE statement, got: {sql}")
        table_asts.append(ast)

    values_asts: list[exp.Insert] = []
    for sql in insert_sqls:
        ast = sqlglot.parse_one(sql, dialect=Dialect.POSTGRES.get_sqlglot_dialect())
        if not isinstance(ast, exp.Insert):
            raise ValueError(f"Expected INSERT INTO statement, got: {sql}")
        values_asts.append(ast)

    catalog = build_catalog_from_sql("; ".join(create_sqls))
    
    return catalog, table_asts, values_asts
