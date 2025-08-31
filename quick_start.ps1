# Quick Start Script for Green Hydrogen Credit System
Write-Host "🚀 QUICK START - Green Hydrogen Credit System" -ForegroundColor Green
Write-Host "Starting both servers..." -ForegroundColor Yellow

# Start Backend
Write-Host "🔧 Starting Backend Server..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'f:\project Hydro\Blockchain-Based-Green-Hydrogen-Credit-System-\backend'; python test_simple.py"

# Wait for backend
Start-Sleep -Seconds 5

# Start Frontend
Write-Host "🎨 Starting Frontend Server..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'f:\project Hydro\Blockchain-Based-Green-Hydrogen-Credit-System-\client'; npm start"

Write-Host "✅ Both servers are starting!" -ForegroundColor Green
Write-Host "🌐 Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "🔧 Backend: http://localhost:5000" -ForegroundColor Cyan
Write-Host "🧠 ML Verification: http://localhost:3000/ngo-dashboard" -ForegroundColor Cyan

Write-Host "🛒 Buyer Dashboard: http://localhost:3000/buyer-dashboard" -ForegroundColor Cyan
Write-Host "🎯 System should be ready in 30 seconds!" -ForegroundColor Green

