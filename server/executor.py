from typing import List, Tuple, Any

from config import SQLITE_PATH
from db import open_ro_conn

def enforce_limit(sql: str, row_limit: int = 1000) -> str:
    if "limit" not in sql.lower():
        sql += f" LIMIT {row_limit}"
    return sql

def execute_sql(sql: str, db_path: str = SQLITE_PATH, row_limit: int = 1000, timeout: float = 5.0) -> Tuple[List[str], List[Tuple[Any]]]:
    sql = enforce_limit(sql, row_limit)
    conn = open_ro_conn(db_path)
    conn.execute(f"PRAGMA busy_timeout = {int(timeout*1000)};")
    cur = conn.cursor()
    cur.execute(sql)
    cols = [c[0] for c in cur.description] if cur.description else []
    rows = cur.fetchmany(row_limit)
    conn.close()
    return cols, rows