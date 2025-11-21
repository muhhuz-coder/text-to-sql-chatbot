import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Import the core RAG components
from rag_pipeline import retriever_node, sql_generator_node
from server.sql_validator import validate_sql
from server.executor import execute_sql
from server.utils import allowed_tables_from_db

load_dotenv()
SQLITE_PATH = os.getenv("SQLITE_PATH", "sample_db/sample.db")
ALLOWED_TABLES = allowed_tables_from_db(SQLITE_PATH)

app = FastAPI(title="RAG Text->SQL API")

class QueryRequest(BaseModel):
    question: str
    show_sql: bool = True

@app.post("/query")
async def query(req: QueryRequest):
    state = {"question": req.question, "messages": []}
    # 1. retrieve
    state = await retriever_node(state)
    # 2. generate SQL
    state = await sql_generator_node(state)
    sql = state["generated_sql"]
    ok, reason = validate_sql(sql, ALLOWED_TABLES)
    if not ok:
        raise HTTPException(status_code=400, detail=f"SQL validation failed: {reason}. SQL: {sql}")
    # 3. execute
    cols, rows = execute_sql(sql, SQLITE_PATH)
    # format result rows
    result = [dict(zip(cols, r)) for r in rows]
    return {"sql": sql if req.show_sql else None, "cols": cols, "rows": result}