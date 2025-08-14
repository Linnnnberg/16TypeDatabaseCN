from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import make_url
from typing import Generator
import os
from app.core.config import settings
from app.database.models import Base

# Create engine with SQLite for prototype
# If using SQLite, ensure directory exists for relative paths and set connect args
if settings.database_url.startswith("sqlite"):
    url = make_url(settings.database_url)
    database_path = url.database or ""
    if database_path:
        directory_path = os.path.dirname(database_path)
        # Only attempt to create directories for non-absolute paths
        if directory_path and not os.path.isabs(directory_path):
            os.makedirs(directory_path, exist_ok=True)
    engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
else:
    engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables() -> None:
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
