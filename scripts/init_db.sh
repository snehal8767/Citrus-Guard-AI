#!/usr/bin/env bash
# Initialize / migrate the database, seed demo data, train the demo model (macOS/Linux).
set -e
cd "$(dirname "$0")/../backend"
source .venv/bin/activate
alembic upgrade head
python -m app.database.seed
python -m app.ai.train_demo_model
echo "Database ready."
