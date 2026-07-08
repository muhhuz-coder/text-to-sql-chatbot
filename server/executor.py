import sqlite3
from typing import List, Tuple, Any

class SQLExecutionError(Exception):
    """Raised when a SQL statement fails to execute against the database."""

def enforce_limit(sql: str, row_limit: int = 1000) -> str:
    if "limit" not in sql.lower():
        sql += f" LIMIT {row_limit}"
    return sql

def open_ro_conn(db_path: str):
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    return conn

def execute_sql(sql: str, db_path: str = "sample_db/sample.db", row_limit: int = 1000, timeout: float = 5.0) -> Tuple[List[str], List[Tuple[Any]]]:
    sql = enforce_limit(sql, row_limit)
    conn = open_ro_conn(db_path)
    try:
        conn.execute(f"PRAGMA busy_timeout = {int(timeout*1000)};")
        cur = conn.cursor()
        cur.execute(sql)
        cols = [c[0] for c in cur.description] if cur.description else []
        rows = cur.fetchmany(row_limit)
        return cols, rows
    except sqlite3.Error as e:
        raise SQLExecutionError(f"failed to execute query: {e}") from e
    finally:
        conn.close()
