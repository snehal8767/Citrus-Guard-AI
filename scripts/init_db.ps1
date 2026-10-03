# Initialize / migrate the database, seed demo data, train the demo model (Windows).
$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..\backend")
.\.venv\Scripts\Activate.ps1
alembic upgrade head
python -m app.database.seed
python -m app.ai.train_demo_model
Write-Host "Database ready."
