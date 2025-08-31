# Minimal Test - Isolate the connection issue
Write-Host "MINIMAL TEST: Testing basic connectivity..." -ForegroundColor Magenta

# Test 1: Can we reach localhost:5000 at all?
Write-Host "Test 1: Basic port connectivity..." -ForegroundColor Yellow
try {
    $tcpClient = New-Object System.Net.Sockets.TcpClient
    $tcpClient.Connect("localhost", 5000)
    $tcpClient.Close()
    Write-Host "Port 5000 is reachable" -ForegroundColor Green
} catch {
    Write-Host "Port 5000 is not reachable: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Can we make an HTTP request?
Write-Host "Test 2: HTTP request to backend..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/api/health" -Method Get -TimeoutSec 10
    Write-Host "HTTP request successful: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "Response: $($response.Content)" -ForegroundColor Cyan
} catch {
    Write-Host "HTTP request failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Check if any Python processes are running
Write-Host "Test 3: Checking Python processes..." -ForegroundColor Yellow
$pythonProcesses = Get-Process | Where-Object {$_.ProcessName -eq "python"}
if ($pythonProcesses) {
    Write-Host "Found Python processes:" -ForegroundColor Green
    $pythonProcesses | ForEach-Object { Write-Host "   PID: $($_.Id), Name: $($_.ProcessName)" -ForegroundColor Cyan }
} else {
    Write-Host "No Python processes found" -ForegroundColor Red
}

# Test 4: Check if port 5000 is actually listening
Write-Host "Test 4: Checking if port 5000 is listening..." -ForegroundColor Yellow
$listeningPorts = netstat -an | Select-String ":5000"
if ($listeningPorts) {
    Write-Host "Port 5000 is listening:" -ForegroundColor Green
    $listeningPorts | ForEach-Object { Write-Host "   $_" -ForegroundColor Cyan }
} else {
    Write-Host "Port 5000 is not listening" -ForegroundColor Red
}
