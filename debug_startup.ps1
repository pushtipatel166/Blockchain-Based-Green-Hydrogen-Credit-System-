# Debug Startup Script - Detailed logging
Write-Host "🔍 DEBUG MODE: Starting AI-Powered Green Hydrogen Credit System..." -ForegroundColor Magenta

# Check if Python is available
Write-Host "🐍 Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found or not in PATH" -ForegroundColor Red
    exit 1
}

# Check if Node.js is available
Write-Host "📦 Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✅ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found or not in PATH" -ForegroundColor Red
    exit 1
}

# Check if npm is available
Write-Host "📦 Checking npm installation..." -ForegroundColor Yellow
try {
    $npmVersion = npm --version 2>&1
    Write-Host "✅ npm found: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ npm not found or not in PATH" -ForegroundColor Red
    exit 1
}

# Check current directory
Write-Host "📁 Current directory: $(Get-Location)" -ForegroundColor Cyan

# Check if backend directory exists
if (Test-Path "backend") {
    Write-Host "✅ Backend directory found" -ForegroundColor Green
} else {
    Write-Host "❌ Backend directory not found" -ForegroundColor Red
    exit 1
}

# Check if client directory exists
if (Test-Path "client") {
    Write-Host "✅ Client directory found" -ForegroundColor Green
} else {
    Write-Host "❌ Client directory not found" -ForegroundColor Red
    exit 1
}

# Check if backend requirements are installed
Write-Host "📋 Checking backend dependencies..." -ForegroundColor Yellow
if (Test-Path "backend/venv") {
    Write-Host "✅ Virtual environment found" -ForegroundColor Green
} else {
    Write-Host "⚠️  Virtual environment not found. Creating one..." -ForegroundColor Yellow
    Set-Location backend
    python -m venv venv
    Set-Location ..
}

# Activate virtual environment and install requirements
Write-Host "🔧 Activating virtual environment and installing requirements..." -ForegroundColor Yellow
Set-Location backend
& ".\venv\Scripts\Activate.ps1"
pip install -r requirements.txt
Set-Location ..

# Check if client dependencies are installed
Write-Host "📦 Checking client dependencies..." -ForegroundColor Yellow
if (Test-Path "client/node_modules") {
    Write-Host "✅ Client dependencies found" -ForegroundColor Green
} else {
    Write-Host "⚠️  Installing client dependencies..." -ForegroundColor Yellow
    Set-Location client
    npm install
    Set-Location ..
}

# Kill any existing processes
Write-Host "🧹 Cleaning up existing processes..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -eq "python" -or $_.ProcessName -eq "node"} | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 3

# Start backend with detailed logging
Write-Host "🚀 Starting backend server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; .\venv\Scripts\Activate.ps1; python test_simple.py" -WindowStyle Normal

# Wait for backend to start
Write-Host "⏳ Waiting for backend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Test backend connectivity
Write-Host "🧪 Testing backend connectivity..." -ForegroundColor Cyan
$maxAttempts = 10
$attempt = 0
$backendReady = $false

while ($attempt -lt $maxAttempts -and -not $backendReady) {
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:5000/api/health" -Method Get -TimeoutSec 5
        Write-Host "✅ Backend is responding: $($response.status)" -ForegroundColor Green
        $backendReady = $true
    } catch {
        $attempt++
        Write-Host "⏳ Attempt $attempt/$maxAttempts - Backend not ready yet..." -ForegroundColor Yellow
        Start-Sleep -Seconds 3
    }
}

if ($backendReady) {
    # Start frontend
    Write-Host "🎨 Starting frontend server..." -ForegroundColor Green
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd client; npm start" -WindowStyle Normal
    
    # Wait for frontend to start
    Start-Sleep -Seconds 15
    
    Write-Host "✅ System started successfully!" -ForegroundColor Green
    Write-Host "🌐 Frontend: http://localhost:3000" -ForegroundColor Cyan
    Write-Host "🔧 Backend: http://localhost:5000" -ForegroundColor Cyan
    
    # Open browser
    Start-Process "http://localhost:3000"
} else {
    Write-Host "❌ Backend failed to start properly" -ForegroundColor Red
    Write-Host "🔍 Check the backend console for error messages" -ForegroundColor Yellow
}
