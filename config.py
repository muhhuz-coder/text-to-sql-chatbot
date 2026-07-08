"""Centralized configuration loaded from environment variables.

Importing this module loads the ``.env`` file once and exposes the shared
settings used across the indexing script, RAG pipeline and API server.
"""
import os

from dotenv import load_dotenv

load_dotenv()

SQLITE_PATH = os.getenv("SQLITE_PATH", "sample_db/sample.db")
CHROMA_DIR = os.getenv("CHROMA_DIR", "./chroma_persist")
EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
TOP_K = int(os.getenv("TOP_K", "8"))

# Name of the Chroma collection shared by the indexer and the retriever.
CHROMA_COLLECTION = "sqlite_docs"
