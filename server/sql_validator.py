import sqlglot
from typing import Set, Tuple

DISALLOWED = {"delete", "update", "insert", "drop", "alter", "create", "truncate", "exec", "execute"}
ALLOWED_STATEMENTS = {"select"}

def validate_sql(sql: str, allowed_tables: Set[str]) -> Tuple[bool, str]:
    if not sql or not sql.strip():
        return False, "no SQL was generated"
    if ";" in sql:
        return False, "semicolon or multiple statements not allowed"
    for kw in DISALLOWED:
        if f" {kw} " in f" {sql.lower()} ":
            return False, f"disallowed keyword: {kw}"

    try:
        parsed = sqlglot.parse_one(sql, read="sqlite")
    except Exception as e:
        return False, f"sql parse error: {e}"

    if parsed.key.lower() not in ALLOWED_STATEMENTS:
        return False, "only SELECT statements allowed"

    try:
        tables = extract_tables(parsed)
    except Exception as e:
        return False, f"could not determine tables referenced: {e}"

    if not tables.issubset(allowed_tables):
        return False, f"disallowed tables used: {tables - allowed_tables}"
    return True, "ok"

def extract_tables(parsed: sqlglot.exp.Expression) -> Set[str]:
    """Collect the table names referenced by an already-parsed expression.

    A parse failure here would previously be swallowed and reported as "no
    tables", which silently bypassed the allow-list check. Errors are now
    surfaced to the caller instead.
    """
    return {table.name for table in parsed.find_all(sqlglot.exp.Table)}
