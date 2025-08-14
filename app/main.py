import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# Import database
from app.database.database import create_tables

# Import API routers
from app.api.auth import router as auth_router
from app.api.celebrities import router as celebrities_router
from app.api.votes import router as votes_router
from app.api.comments import router as comments_router
from app.api.uploads import router as uploads_router
from app.api.search import router as search_router
from app.api.mbti import router as mbti_router

# Create FastAPI application
app = FastAPI(title="16型花名册", description="MBTI人格类型数据库API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Include API routers
app.include_router(auth_router)
app.include_router(celebrities_router)
app.include_router(votes_router)
app.include_router(comments_router)
app.include_router(uploads_router)
app.include_router(search_router)
app.include_router(mbti_router)


# Template routes
@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    """Homepage with hero section and features"""
    from app.data.mbti_types import get_all_types_with_info

    try:
        mbti_types = get_all_types_with_info()
        return templates.TemplateResponse(
            "index.html", {"request": request, "mbti_types": mbti_types}
        )
    except Exception as e:
        # Fallback to empty list if there's an error
        return templates.TemplateResponse(
            "index.html", {"request": request, "mbti_types": []}
        )


@app.get("/test", response_class=HTMLResponse)
async def test_page(request: Request):
    """MBTI test page"""
    return templates.TemplateResponse("test.html", {"request": request})


@app.get("/result", response_class=HTMLResponse)
async def result_page(request: Request):
    """Test result page"""
    return templates.TemplateResponse("result.html", {"request": request})


@app.get("/celebrities", response_class=HTMLResponse)
async def celebrities_page(request: Request):
    """Celebrities directory page"""
    return templates.TemplateResponse("celebrities.html", {"request": request})


@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    """About MBTI page"""
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/test-frontend", response_class=HTMLResponse)
async def test_frontend_page(request: Request):
    """Frontend test page for debugging"""
    with open("test_frontend.html", "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content=content)


# API root path
@app.get("/api")
def read_root():
    return {
        "message": "欢迎使用16型花名册API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}


# Test endpoint
@app.get("/test")
def test_endpoint():
    return {
        "message": "API is working!",
        "mbti_types": [
            "INTJ",
            "INTP",
            "ENTJ",
            "ENTP",
            "INFJ",
            "INFP",
            "ENFJ",
            "ENFP",
            "ISTJ",
            "ISFJ",
            "ESTJ",
            "ESFJ",
            "ISTP",
            "ISFP",
            "ESTP",
            "ESFP",
        ],
    }


# Database test endpoint
@app.get("/db-test")
def test_database():
    try:
        # Try to create tables
        create_tables()
        return {
            "status": "success",
            "message": "Database connection and tables created successfully",
            "tables": [
                "users",
                "celebrities",
                "votes",
                "comments",
                "tags",
                "celebrity_tags",
                "daily_user_stats",
            ],
        }
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}


# Environment info
@app.get("/env")
def env_info():
    return {
        "python_version": os.sys.version,
        "fastapi_version": "0.104.1",
        "environment": "local_development",
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        create_tables()
        print("Database tables created successfully")
    except Exception as e:
        print(f"Database initialization error: {e}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
