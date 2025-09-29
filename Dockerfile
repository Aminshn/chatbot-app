# syntax=docker/dockerfile:1

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System deps
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps first (better cache)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY app.py /app/app.py

# Expose Streamlit default port
EXPOSE 8501

# Streamlit runtime settings
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_SERVER_ENABLECORS=false \
    STREAMLIT_SERVER_ENABLEXSRSFPROTECTION=false \
    STREAMLIT_SERVER_HEADLESS=true

# Ollama server location (used by python ollama client)
ENV OLLAMA_HOST=http://ollama:11434

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
