#!/usr/bin/env bash
# Reset demo data to the deterministic story (macOS/Linux).
set -e
cd "$(dirname "$0")/../backend"
source .venv/bin/activate
python -m app.database.seed --reset
echo "Demo data reset."
