import sqlite3
from typing import Set

def allowed_tables_from_db(db_path: str) -> Set[str]:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = {t[0] for t in cur.fetchall()}
    conn.close()
    return tables