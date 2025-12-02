# Start the FastAPI experimental server
# This runs the API on port 8000 (Streamlit runs on 8501)

Write-Host "Starting COVID-19 Vaccine Tracker API (Experimental)..." -ForegroundColor Green
Write-Host "API will be available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Docs available at: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Navigate to project root
Set-Location $PSScriptRoot\..\..\

# Start uvicorn
uvicorn app.experimental.main:app --reload --port 8000 --host 0.0.0.0
