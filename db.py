"""Shared SQLite helpers.

Connection handling and the "list user tables" query were previously
duplicated across ``main.py``, ``server/utils.py`` and ``server/executor.py``.
They now live here.
"""
import sqlite3
from typing import List, Set

from config import SQLITE_PATH

# Lists user-defined tables, excluding SQLite's internal ``sqlite_*`` tables.
_LIST_TABLES_QUERY = (
    "SELECT name FROM sqlite_master "
    "WHERE type='table' AND name NOT LIKE 'sqlite_%'"
)


def connect(db_path: str = SQLITE_PATH) -> sqlite3.Connection:
    """Open a standard read/write connection to the SQLite database."""
    return sqlite3.connect(db_path)


def open_ro_conn(db_path: str = SQLITE_PATH) -> sqlite3.Connection:
    """Open a read-only connection to the SQLite database."""
    return sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)


def list_tables(conn: sqlite3.Connection) -> List[str]:
    """Return the user-defined table names for an open connection."""
    cur = conn.cursor()
    cur.execute(_LIST_TABLES_QUERY)
    return [row[0] for row in cur.fetchall()]


def allowed_tables_from_db(db_path: str = SQLITE_PATH) -> Set[str]:
    """Return the set of user-defined tables in the database at ``db_path``."""
    conn = connect(db_path)
    try:
        return set(list_tables(conn))
    finally:
        conn.close()
