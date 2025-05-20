# Streaming Recipe Chatbot Demo 🍲

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-green)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

A minimal FastAPI demo showing real-time LLM streaming with:
- Pre-stream messages
- Token-by-token delivery
- Post-stream messages and background processing

## 🚀 Quick Start

1. Clone the repo & install dependency
    ```bash
    git clone https://github.com/cintiaching/streaming-recipe-chatbot.git
    cd streaming-recipe-chatbot
    uv sync
    source .venv/bin/activate
    ```
2. Set up environment (I am using together.ai free model)
    ```bash
    echo "TOGETHER_API_KEY=your_key" >> .env
    echo "MODEL=meta-llama/Llama-3.3-70B-Instruct-Turbo-Free" >> .env
    ```

3. Run the API
   
   The streaming version:
    ```bash
    uvicorn streaming_app:app --reload --log-level info
   ```
   In a new tab,
   ```bash
   curl -N "http://localhost:8000/recipe/stream/?dish=pasta"
   ```
   Or the not-streaming version:
   ```bash
    uvicorn not_streaming_app.main:app --reload --log-level info
    curl -N "http://localhost:8000/recipe/not_stream/?dish=pasta"
    ```
   The time for running will show in log.
