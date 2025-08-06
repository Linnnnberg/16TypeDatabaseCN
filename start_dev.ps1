# 16型花名册 (MBTI Roster) - Quick Development Startup
# PowerShell script for fast development server startup

Write-Host "16型花名册 (MBTI Roster) - Quick Development Startup" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

# Check if virtual environment exists
if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "Virtual environment not found!" -ForegroundColor Red
    Write-Host "   Please run: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host ".env file not found, creating one..." -ForegroundColor Yellow
    @"
DATABASE_URL=sqlite:///./mbti_roster.db
SECRET_KEY=your-super-secret-key-here-change-in-production
REDIS_URL=redis://localhost:6379
EMAIL_FROM=noreply@mbti-roster.com
"@ | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "   .env file created" -ForegroundColor Green
}

# Check if database and sample data exist
if (-not (Test-Path "mbti_roster.db")) {
    Write-Host "Database not found, creating sample data..." -ForegroundColor Yellow
    
    # Create admin user
    if (Test-Path "create_admin.py") {
        Write-Host "   Creating admin user..." -ForegroundColor Yellow
        & "venv\Scripts\python.exe" create_admin.py
    }
    
    # Create sample celebrities
    if (Test-Path "create_sample_celebrities.py") {
        Write-Host "   Creating sample celebrities..." -ForegroundColor Yellow
        & "venv\Scripts\python.exe" create_sample_celebrities.py
    }
    
    # Create sample votes
    if (Test-Path "create_sample_votes.py") {
        Write-Host "   Creating sample votes..." -ForegroundColor Yellow
        & "venv\Scripts\python.exe" create_sample_votes.py
    }
}

Write-Host "Starting FastAPI server..." -ForegroundColor Green
Write-Host "   Server URL: http://localhost:8000" -ForegroundColor Cyan
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "   Health Check: http://localhost:8000/health" -ForegroundColor Cyan
Write-Host ""
Write-Host "   Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the server
try {
    & "venv\Scripts\uvicorn.exe" app.main:app --host 0.0.0.0 --port 8000 --reload
}
catch {
    Write-Host "Failed to start server: $_" -ForegroundColor Red
    exit 1
} 