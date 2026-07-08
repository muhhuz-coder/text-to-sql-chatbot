import hashlib
import sqlite3

from tqdm import tqdm

from config import SQLITE_PATH
from db import list_tables
from vectorstore import build_vectorstore

# Create / load the shared Chroma vector store
vectorstore = build_vectorstore()


def row_hash(values):
    """Generate unique hash for a row."""
    return hashlib.sha256("|".join(map(str, values)).encode()).hexdigest()


def row_to_text(table, cols, row):
    """Convert SQLite row into a readable text chunk."""
    return f"Table: {table}\n" + "\n".join([f"{c}: {v}" for c, v in zip(cols, row)])


def index_table(conn, table):
    """Index a single table into the vector store."""
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({table});")
    cols = [c[1] for c in cur.fetchall()]
    cur.execute(f"SELECT {', '.join(cols)} FROM {table}")
    rows = cur.fetchall()

    docs, ids, metas = [], [], []
    for r in rows:
        txt = row_to_text(table, cols, r)
        pk = str(r[0])
        hid = row_hash(r)
        ids.append(f"{table}:{pk}")
        docs.append(txt)
        metas.append({"table": table, "pk": pk, "hash": hid})

    # Add to Chroma vector store
    vectorstore.add_texts(texts=docs, metadatas=metas, ids=ids)


def main():
    """Main indexing pipeline."""
    conn = sqlite3.connect(SQLITE_PATH)
    tables = list_tables(conn)

    for t in tqdm(tables, desc="Indexing tables"):
        index_table(conn, t)

    conn.close()
    print("Indexing complete and persisted in Chroma.")


if __name__ == "__main__":
    main()
