#!/usr/bin/env bash
# Start the backend API (macOS/Linux). Swagger: http://localhost:8000/docs
cd "$(dirname "$0")/../backend"
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
