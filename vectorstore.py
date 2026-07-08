"""Factory helpers for the shared embedding model and Chroma vector store.

Both the indexing script (``main.py``) and the RAG pipeline
(``rag_pipeline.py``) need an identically configured embedding model and
Chroma collection; centralizing the construction here keeps them in sync.
"""
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from config import CHROMA_COLLECTION, CHROMA_DIR, EMBED_MODEL


def build_embeddings() -> HuggingFaceEmbeddings:
    """Create the HuggingFace embedding model used throughout the project."""
    return HuggingFaceEmbeddings(model_name=EMBED_MODEL)


def build_vectorstore(embeddings: HuggingFaceEmbeddings | None = None) -> Chroma:
    """Create/load the shared Chroma vector store.

    If ``embeddings`` is not provided a new model is built via
    :func:`build_embeddings`.
    """
    if embeddings is None:
        embeddings = build_embeddings()
    return Chroma(
        collection_name=CHROMA_COLLECTION,
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings,
    )
