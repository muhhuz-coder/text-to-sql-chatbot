import os
import sqlite3
import hashlib
from tqdm import tqdm
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
# Load environment variables
load_dotenv()
SQLITE_PATH = os.getenv("SQLITE_PATH", "sample_db/sample.db")
CHROMA_DIR = os.getenv("CHROMA_DIR", "./chroma_persist")
EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# ✅ Initialize HuggingFace embedding model
embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
print(f"Using embedding model:",embeddings)

# ✅ Create / Load Chroma vector store
vectorstore = Chroma(
    collection_name="sqlite_docs",
    persist_directory=CHROMA_DIR,
    embedding_function=embeddings
)

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
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = [t[0] for t in cur.fetchall()]

    for t in tqdm(tables, desc="Indexing tables"):
        index_table(conn, t)

    conn.close()
    print("Indexing complete and persisted in Chroma.")

if __name__ == "__main__":
    main()