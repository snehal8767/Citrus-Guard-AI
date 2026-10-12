#!/bin/sh
# CitrusGuardAI backend bootstrap (Render or any Linux host).
# 1. apply database migrations
# 2. seed demo data (skips itself if the database is not empty)
# 3. train the demo model if it is missing
# 4. start the API server on the host-assigned port
set -e
PORT="${PORT:-8000}"
alembic upgrade head
python -m app.database.seed
python -m app.ai.train_demo_model
exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
