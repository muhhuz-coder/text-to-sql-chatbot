# Text-to-SQL Chatbot with RAG

This project implements a Retrieval-Augmented Generation (RAG) system that converts natural language questions into SQL queries and executes them against a SQLite database.

## Architecture

- **Data Source**: SQLite database (`sample_db/sample.db`)
- **Embeddings**: Hugging Face embeddings stored in Chroma vector database
- **LLM**: Google Generative AI (Gemini) for SQL generation
- **Backend**: FastAPI for API endpoints
- **Frontend**: Streamlit for user interface

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables in `.env`:
   ```
   SQLITE_PATH=sample_db/sample.db
   CHROMA_DIR=./chroma_persist
   EMBED_MODEL=sentence-transformers/all-MiniLM-L6-v2
   GOOGLE_APPLICATION_CREDENTIALS=text-to-sql-478909-25ed2c97fa6d.json
   LLM_MODEL=gpt-4o-mini
   TOP_K=8
   ```

   For Google Gemini, ensure `GOOGLE_APPLICATION_CREDENTIALS` points to your service account JSON file (currently set to `text-to-sql-478909-25ed2c97fa6d.json`).

3. Create sample database:
   ```bash
   python sample_db/create_sample_db.py
   ```

4. Index the database into Chroma:
   ```bash
   python main.py
   ```

## Running the Application

1. Start the FastAPI backend:
   ```bash
   uvicorn server.api:app --reload --port 8000
   ```

2. Start the Streamlit frontend:
   ```bash
   streamlit run app.py
   ```

3. Open your browser to `http://localhost:8501` and ask questions like "Show total orders per customer".

## Files

- `main.py`: Database indexing script
- `rag_pipeline.py`: Core RAG pipeline (retriever and SQL generator)
- `server/api.py`: FastAPI backend
- `server/sql_validator.py`: SQL validation logic
- `server/executor.py`: Safe SQL execution
- `server/utils.py`: Utility functions
- `app.py`: Streamlit frontend
- `sample_db/create_sample_db.py`: Sample data creation

## Notes

- The system generates read-only SELECT queries only.
- SQL validation ensures only allowed tables are queried.
- For production, consider incremental embeddings and background updates.