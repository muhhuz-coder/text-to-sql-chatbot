FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --index-url https://download.pytorch.org/whl/cpu

# Copy the application code
COPY . .

# Create directories for data
RUN mkdir -p sample_db chroma_persist

# Expose ports for FastAPI and Streamlit
EXPOSE 8000 8501

# Run setup and both services
CMD ["sh", "-c", "python3 create_sample_db.py && python3 main.py && uvicorn server.api:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.port 8501 --server.address 0.0.0.0"]