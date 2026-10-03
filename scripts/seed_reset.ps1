# Reset demo data to the deterministic story (Windows).
$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..\backend")
.\.venv\Scripts\Activate.ps1
python -m app.database.seed --reset
Write-Host "Demo data reset."
