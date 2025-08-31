# Test Backend Connectivity
Write-Host "🧪 Testing Backend Connectivity..." -ForegroundColor Yellow

try {
    # Test health endpoint
    Write-Host "📡 Testing /api/health endpoint..." -ForegroundColor Cyan
    $healthResponse = Invoke-RestMethod -Uri "http://localhost:5000/api/health" -Method Get -TimeoutSec 10
    Write-Host "✅ Health Check: $($healthResponse.status)" -ForegroundColor Green
    
    # Test login endpoint
    Write-Host "📡 Testing /api/login endpoint..." -ForegroundColor Cyan
    $loginData = @{
        username = "testuser"
        password = "testpass"
        role = "buyer"
    } | ConvertTo-Json
    
    $loginResponse = Invoke-RestMethod -Uri "http://localhost:5000/api/login" -Method Post -Body $loginData -ContentType "application/json" -TimeoutSec 10
    Write-Host "✅ Login Test: $($loginResponse.success)" -ForegroundColor Green
    
    # Test buyer credits endpoint
    Write-Host "📡 Testing /api/buyer/credits endpoint..." -ForegroundColor Cyan
    $creditsResponse = Invoke-RestMethod -Uri "http://localhost:5000/api/buyer/credits" -Method Get -TimeoutSec 10
    Write-Host "✅ Credits Test: Found $($creditsResponse.data.Count) credits" -ForegroundColor Green
    
    Write-Host "🎉 All backend tests passed!" -ForegroundColor Green
    Write-Host "🔧 Backend is working correctly on http://localhost:5000" -ForegroundColor Cyan
    
} catch {
    Write-Host "❌ Backend test failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "🔍 Make sure the backend server is running on port 5000" -ForegroundColor Yellow
}
