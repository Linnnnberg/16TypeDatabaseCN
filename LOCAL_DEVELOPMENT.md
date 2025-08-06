# Local Development Guide

## Quick Start (5 minutes)

### Prerequisites
- Python 3.8+ installed
- No database setup required (uses SQLite for local development)

### Step 1: Install Dependencies
```bash
# Install basic dependencies for local development
pip install -r requirements_local.txt
```

### Step 2: Run the Application
```bash
# Option 1: Use the local development script
python run_local.py

# Option 2: Run directly with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Access the Application
- **Main API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Test Endpoint**: http://localhost:8000/test

## What's Working Now

### Available Features
- Basic FastAPI application running
- CORS middleware configured
- Static files and templates setup
- Health check endpoint
- Test endpoint with MBTI types
- Auto-reload on code changes

### Coming Soon
- User authentication
- Database models
- API endpoints
- Frontend interface

## Development Workflow

### Making Changes
1. Edit files in the `app/` directory
2. Save the file
3. The server will automatically reload
4. Check the changes at http://localhost:8000

### Adding New Endpoints
1. Edit `app/main.py` or create new files in `app/api/`
2. Save the file
3. The endpoint will be available immediately

### Debugging
- Check the terminal for error messages
- Use the `/docs` endpoint to test API endpoints
- Check `/health` for application status

## Project Structure (Local Development)

```
16TypeDatabaseCN/
├── app/
│   ├── main.py          # Main FastAPI application
│   ├── core/
│   │   ├── config.py    # Configuration settings
│   │   └── security.py  # Security utilities
│   └── ...
├── requirements_local.txt  # Local development dependencies
├── run_local.py           # Local development startup script
└── LOCAL_DEVELOPMENT.md   # This file
```

## Next Steps

Once the basic application is running locally, you can:

1. **Add Database Support**: Implement SQLite/PostgreSQL models
2. **Add Authentication**: Implement user registration/login
3. **Add API Endpoints**: Create celebrity and voting endpoints
4. **Add Frontend**: Create web interface
5. **Add Advanced Features**: Comments, tags, etc.

## Troubleshooting

### Port Already in Use
```bash
# Use a different port
uvicorn app.main:app --reload --port 8001
```

### Import Errors
```bash
# Make sure you're in the project root directory
cd 16TypeDatabaseCN
python run_local.py
```

### Permission Issues (Windows)
```bash
# Run PowerShell as Administrator or use
python -m uvicorn app.main:app --reload
```

## Support

If you encounter issues:
1. Check the terminal output for error messages
2. Verify Python version (3.8+)
3. Make sure all dependencies are installed
4. Check that you're in the correct directory 