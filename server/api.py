import logging
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Import the core RAG components
from rag_pipeline import retriever_node, sql_generator_node
from server.sql_validator import validate_sql
from server.executor import execute_sql, SQLExecutionError
from server.utils import allowed_tables_from_db

logger = logging.getLogger(__name__)

load_dotenv()
SQLITE_PATH = os.getenv("SQLITE_PATH", "sample_db/sample.db")
ALLOWED_TABLES = allowed_tables_from_db(SQLITE_PATH)

app = FastAPI(title="RAG Text->SQL API")

class QueryRequest(BaseModel):
    question: str
    show_sql: bool = True

@app.post("/query")
async def query(req: QueryRequest):
    if not req.question or not req.question.strip():
        raise HTTPException(status_code=400, detail="question must not be empty")

    state = {"question": req.question, "messages": []}

    # 1. retrieve + 2. generate SQL
    try:
        state = await retriever_node(state)
        state = await sql_generator_node(state)
    except Exception as e:
        logger.exception("RAG pipeline failed for question: %s", req.question)
        raise HTTPException(status_code=502, detail=f"failed to generate SQL: {e}") from e

    sql = state.get("generated_sql", "")

    ok, reason = validate_sql(sql, ALLOWED_TABLES)
    if not ok:
        raise HTTPException(status_code=400, detail=f"SQL validation failed: {reason}. SQL: {sql}")

    # 3. execute
    try:
        cols, rows = execute_sql(sql, SQLITE_PATH)
    except SQLExecutionError as e:
        raise HTTPException(status_code=400, detail=f"{e}. SQL: {sql}") from e
    except Exception as e:
        logger.exception("Unexpected error executing SQL: %s", sql)
        raise HTTPException(status_code=500, detail=f"internal error executing query: {e}") from e

    # format result rows
    result = [dict(zip(cols, r)) for r in rows]
    return {"sql": sql if req.show_sql else None, "cols": cols, "rows": result}
