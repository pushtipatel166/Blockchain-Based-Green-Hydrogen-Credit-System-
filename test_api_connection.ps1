# Test API Connection between Frontend and Backend
Write-Host "Testing API Connection..." -ForegroundColor Magenta

# Test 1: Direct backend API call
Write-Host "Test 1: Direct backend API call..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:5000/api/health" -Method Get
    Write-Host "Backend API working: $($response.status)" -ForegroundColor Green
} catch {
    Write-Host "Backend API failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Test login endpoint
Write-Host "Test 2: Testing login endpoint..." -ForegroundColor Yellow
try {
    $loginData = @{
        username = "testuser"
        password = "testpass"
        role = "buyer"
    } | ConvertTo-Json
    
    $loginResponse = Invoke-RestMethod -Uri "http://localhost:5000/api/login" -Method Post -Body $loginData -ContentType "application/json"
    Write-Host "Login API working: $($loginResponse.success)" -ForegroundColor Green
} catch {
    Write-Host "Login API failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Test if frontend can reach backend through browser
Write-Host "Test 3: Testing CORS and browser compatibility..." -ForegroundColor Yellow
try {
    # Simulate a browser request with proper headers
    $headers = @{
        'Origin' = 'http://localhost:3000'
        'User-Agent' = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        'Accept' = 'application/json'
    }
    
    $corsResponse = Invoke-RestMethod -Uri "http://localhost:5000/api/health" -Method Get -Headers $headers
    Write-Host "CORS test successful: $($corsResponse.status)" -ForegroundColor Green
} catch {
    Write-Host "CORS test failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "API connection test completed!" -ForegroundColor Cyan
