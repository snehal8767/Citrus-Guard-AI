# CitrusGuardAI setup (Windows PowerShell). Run from the project root.
$ErrorActionPreference = "Stop"
Write-Host "==> Backend setup..."
Set-Location backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
if (-not (Test-Path .env)) { Copy-Item ..\.env.example .env }
if (-not (Test-Path ..\.env)) { Copy-Item ..\.env.example ..\.env }
Set-Location ..
Write-Host "==> Frontend setup..."
Set-Location frontend
npm install
Set-Location ..
Write-Host "Done. Next: scripts\init_db.ps1"
