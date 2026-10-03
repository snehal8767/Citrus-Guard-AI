#!/usr/bin/env bash
# CitrusGuardAI setup (macOS/Linux). Run from the project root.
set -e
echo "==> Backend setup..."
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
[ -f .env ] || cp ../.env.example .env
[ -f ../.env ] || cp ../.env.example ../.env
cd ..
echo "==> Frontend setup..."
cd frontend
npm install
cd ..
echo "Done. Next: scripts/init_db.sh"
