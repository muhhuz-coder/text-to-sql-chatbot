"""Backwards-compatible re-export of the shared SQLite helpers.

The implementation now lives in the top-level :mod:`db` module so it can be
shared with the indexing script; this module is kept so existing imports of
``server.utils`` continue to work.
"""
from db import allowed_tables_from_db

__all__ = ["allowed_tables_from_db"]
