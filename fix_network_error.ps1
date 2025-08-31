# Fix Network Error - H2Credits System
Write-Host "FIXING NETWORK ERROR: H2Credits System..." -ForegroundColor Magenta

# Step 1: Kill existing processes
Write-Host "Step 1: Cleaning up existing processes..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -eq "python" -or $_.ProcessName -eq "node"} | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 3

# Step 2: Start backend
Write-Host "Step 2: Starting backend server..." -ForegroundColor Yellow
Set-Location backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python test_simple.py" -WindowStyle Normal
Set-Location ..

# Step 3: Wait for backend
Write-Host "Step 3: Waiting for backend to be ready..." -ForegroundColor Yellow
$maxAttempts = 20
$attempt = 0
$backendReady = $false

while ($attempt -lt $maxAttempts -and -not $backendReady) {
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:5000/api/health" -Method Get -TimeoutSec 5
        if ($response.status -eq "OK" -or $response.status -eq "healthy") {
            Write-Host "Backend is ready!" -ForegroundColor Green
            $backendReady = $true
        }
    } catch {
        $attempt++
        Write-Host "Waiting for backend... Attempt $attempt/$maxAttempts" -ForegroundColor Yellow
        Start-Sleep -Seconds 2
    }
}

if (-not $backendReady) {
    Write-Host "Backend failed to start. Check the backend console." -ForegroundColor Red
    exit 1
}

# Step 4: Start frontend
Write-Host "Step 4: Starting frontend server..." -ForegroundColor Yellow
Set-Location client
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm start" -WindowStyle Normal
Set-Location ..

# Step 5: Wait and test
Write-Host "Step 5: Waiting for frontend..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

try {
    $frontendResponse = Invoke-WebRequest -Uri "http://localhost:3000" -Method Get -TimeoutSec 10
    Write-Host "Frontend is accessible: $($frontendResponse.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "Frontend test failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Step 6: Final check
Write-Host "Step 6: Final verification..." -ForegroundColor Yellow
$backendCheck = netstat -ano | Select-String "5000" | Select-String "LISTENING"
$frontendCheck = netstat -ano | Select-String "3000" | Select-String "LISTENING"

if ($backendCheck -and $frontendCheck) {
    Write-Host "SUCCESS! Both servers are running:" -ForegroundColor Green
    Write-Host "Backend: http://localhost:5000" -ForegroundColor Cyan
    Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
    Write-Host "Opening browser..." -ForegroundColor Yellow
    
    Start-Sleep -Seconds 3
    Start-Process "http://localhost:3000"
    
    Write-Host "If you still see 'Failed to fetch' error:" -ForegroundColor Yellow
    Write-Host "1. Check browser console (F12) for detailed error messages" -ForegroundColor White
    Write-Host "2. Try refreshing the page after a few seconds" -ForegroundColor White
    Write-Host "3. Check if any browser extensions are blocking requests" -ForegroundColor White
    Write-Host "4. Try opening in an incognito/private window" -ForegroundColor White
} else {
    Write-Host "FAILED: One or both servers are not running properly" -ForegroundColor Red
}
