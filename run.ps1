# CitrusGuardAI — one-command startup (Windows PowerShell).
# Run from the project root:   .\run.ps1
# Opens TWO new windows: backend API (:8000) + frontend (:5173). Keep them open.

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendDir = Join-Path $Root "backend"
$FrontendDir = Join-Path $Root "frontend"
$VenvPy = Join-Path $BackendDir ".venv\Scripts\python.exe"

function Fail($msg) { Write-Host "ERROR: $msg" -ForegroundColor Red; exit 1 }

function PortOpen($port) {
    $c = New-Object Net.Sockets.TcpClient
    try { $c.Connect("127.0.0.1", $port); $c.Close(); return $true }
    catch { return $false }
}

# ---- Preflight checks (exact paths, no guessing) ----
if (-not (Test-Path $VenvPy)) { Fail "backend .venv missing. Run: scripts\setup.ps1" }
if (-not (Test-Path (Join-Path $BackendDir ".env"))) { Fail "backend\.env missing. Run: Copy-Item .env.example backend\.env" }
if (-not (Test-Path (Join-Path $FrontendDir "node_modules"))) { Fail "frontend\node_modules missing. Run: cd frontend; npm install" }

# ---- Database: auto-init if missing ----
if (-not (Test-Path (Join-Path $BackendDir "data\citrusguard.db"))) {
    Write-Host "Database not found - creating (migrate + seed + train)..." -ForegroundColor Yellow
    Push-Location $BackendDir
    & $VenvPy -m alembic upgrade head
    & $VenvPy -m app.database.seed
    & $VenvPy -m app.ai.train_demo_model
    Pop-Location
}

# ---- Already running? ----
$back = PortOpen 8000
$front = PortOpen 5173
if ($back -and $front) {
    Write-Host "Already running. Open http://localhost:5173 (farmer / farmer123)" -ForegroundColor Green
    exit 0
}
if ($back) { Write-Host "Port 8000 busy by something else. Stop it or change the port." -ForegroundColor Yellow }
if ($front) { Write-Host "Port 5173 busy by something else. Stop it or change the port." -ForegroundColor Yellow }

# ---- Start both servers in new windows (logs stay visible) ----
if (-not $back) {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$BackendDir'; .\.venv\Scripts\Activate.ps1; python -m uvicorn app.main:app --port 8000"
    Write-Host "Backend starting in new window..." -ForegroundColor Green
}
if (-not $front) {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$FrontendDir'; npm.cmd run dev"
    Write-Host "Frontend starting in new window..." -ForegroundColor Green
}

Write-Host ""
Write-Host "App:      http://localhost:5173   (farmer / farmer123)" -ForegroundColor Cyan
Write-Host "API docs: http://localhost:8000/docs" -ForegroundColor Cyan
