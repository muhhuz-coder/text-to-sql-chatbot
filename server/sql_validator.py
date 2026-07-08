import sqlglot
from typing import Set, Tuple

DISALLOWED = {"delete", "update", "insert", "drop", "alter", "create", "truncate", "exec", "execute"}
ALLOWED_STATEMENTS = {"select"}

def validate_sql(sql: str, allowed_tables: Set[str]) -> Tuple[bool, str]:
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

    tables = _tables_from_parsed(parsed)
    if not tables.issubset(allowed_tables):
        return False, f"disallowed tables used: {tables - allowed_tables}"
    return True, "ok"

def extract_tables(sql: str) -> Set[str]:
    try:
        parsed = sqlglot.parse_one(sql, read="sqlite")
    except Exception:
        return set()
    return _tables_from_parsed(parsed)

def _tables_from_parsed(parsed: sqlglot.exp.Expression) -> Set[str]:
    return {table.name for table in parsed.find_all(sqlglot.exp.Table)}
