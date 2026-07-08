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

- `config.py`: Centralized environment/configuration loading
- `vectorstore.py`: Shared embedding model and Chroma vector store factory
- `db.py`: Shared SQLite connection and table-listing helpers
- `main.py`: Database indexing script
- `rag_pipeline.py`: Core RAG pipeline (retriever and SQL generator)
- `server/api.py`: FastAPI backend
- `server/sql_validator.py`: SQL validation logic
- `server/executor.py`: Safe SQL execution
- `server/utils.py`: Utility functions
- `app.py`: Streamlit frontend
- `sample_db/create_sample_db.py`: Sample data creation

## Deployment

### Local with Docker
1. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```
2. Access:
   - FastAPI: http://localhost:8000
   - Streamlit: http://localhost:8501

### Cloud Deployment
#### Option 1: Railway (Free tier available)
1. Push your code to GitHub.
2. Go to [Railway.app](https://railway.app), connect your GitHub repo.
3. Set environment variables in Railway dashboard.
4. Deploy – it will auto-detect Python and run.

#### Option 2: Render
1. Push to GitHub.
2. Go to [Render.com](https://render.com), create a new Web Service from GitHub.
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn server.api:app --host 0.0.0.0 --port $PORT`
5. For Streamlit, deploy separately to Streamlit Cloud.

#### Option 3: Streamlit Cloud (for frontend only)
1. Push to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io), connect repo.
3. Set main file to `app.py`.
4. Add secrets for environment variables.

### Environment Variables
Set these in your deployment platform's environment settings:
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to your service account JSON (upload as secret or file).
- `SQLITE_PATH`, `CHROMA_DIR`, etc.

For production, consider using a persistent database like PostgreSQL instead of SQLite.