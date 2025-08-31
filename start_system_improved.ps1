# Start AI-Powered Green Hydrogen Credit System - IMPROVED VERSION
Write-Host "🚀 Starting AI-Powered Green Hydrogen Credit System..." -ForegroundColor Green

# Function to check if a port is available
function Test-Port {
    param([int]$Port)
    try {
        $connection = New-Object System.Net.Sockets.TcpClient
        $connection.Connect("localhost", $Port)
        $connection.Close()
        return $true
    }
    catch {
        return $false
    }
}

# Function to wait for backend to be ready
function Wait-ForBackend {
    $maxAttempts = 30
    $attempt = 0
    
    Write-Host "⏳ Waiting for backend to be ready..." -ForegroundColor Yellow
    
    while ($attempt -lt $maxAttempts) {
        try {
            $response = Invoke-RestMethod -Uri "http://localhost:5000/api/health" -Method Get -TimeoutSec 5
            if ($response.status -eq "OK" -or $response.status -eq "healthy") {
                Write-Host "✅ Backend is ready!" -ForegroundColor Green
                return $true
            }
        }
        catch {
            # Continue waiting
        }
        
        $attempt++
        Start-Sleep -Seconds 2
        Write-Host "⏳ Attempt $attempt/$maxAttempts - Waiting for backend..." -ForegroundColor Yellow
    }
    
    Write-Host "❌ Backend failed to start within expected time" -ForegroundColor Red
    return $false
}

# Kill any existing processes on ports 5000 and 3000
Write-Host "🧹 Cleaning up existing processes..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -eq "python" -or $_.ProcessName -eq "node"} | Stop-Process -Force -ErrorAction SilentlyContinue

# Wait a moment for cleanup
Start-Sleep -Seconds 2

# Start Backend Server
Write-Host "🔧 Starting Backend Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; python test_simple.py" -WindowStyle Minimized

# Wait for backend to be ready
if (Wait-ForBackend) {
    # Start Frontend Server
    Write-Host "🎨 Starting Frontend Server..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd client; npm start" -WindowStyle Minimized
    
    # Wait for frontend to start
    Start-Sleep -Seconds 10
    
    Write-Host "✅ System Started Successfully!" -ForegroundColor Green
    Write-Host "🌐 Frontend URL: http://localhost:3000" -ForegroundColor Cyan
    Write-Host "🔧 Backend URL: http://localhost:5000" -ForegroundColor Cyan
    Write-Host "🧠 ML Verification: http://localhost:3000/ngo-dashboard" -ForegroundColor Cyan
    Write-Host "🛒 Buyer Dashboard: http://localhost:3000/buyer-dashboard" -ForegroundColor Cyan
    Write-Host "🎯 Your AI-Powered Green Hydrogen Credit System is ready!" -ForegroundColor Green
    
    # Open the frontend in default browser
    Start-Sleep -Seconds 5
    Start-Process "http://localhost:3000"
} else {
    Write-Host "❌ Failed to start system. Backend is not responding." -ForegroundColor Red
    Write-Host "🔍 Check the backend console for error messages." -ForegroundColor Yellow
}
