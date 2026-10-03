# Start the backend API (Windows). Swagger: http://localhost:8000/docs
Set-Location (Join-Path $PSScriptRoot "..\backend")
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
