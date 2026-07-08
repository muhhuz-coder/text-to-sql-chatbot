import os
import sqlite3
from typing import Set

def allowed_tables_from_db(db_path: str) -> Set[str]:
    if not os.path.exists(db_path):
        raise FileNotFoundError(
            f"database not found at {db_path!r}; create it before starting the API"
        )
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = {t[0] for t in cur.fetchall()}
    finally:
        conn.close()
    return tables
