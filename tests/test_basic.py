"""
Basic pytest tests for MBTI Roster
These tests can run in CI environment without requiring a running server
"""
import pytest
import sys
import os
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.database.models import User, Celebrity, Vote, Comment, Tag, MBTIType
from app.schemas.auth import UserCreate, UserLogin, Token
from app.schemas.celebrity import CelebrityCreate, CelebrityUpdate
from app.schemas.vote import VoteCreate
from app.schemas.comment import CommentCreate

def test_imports():
    """Test that all required modules can be imported"""
    assert User is not None
    assert Celebrity is not None
    assert Vote is not None
    assert Comment is not None
    assert Tag is not None
    assert MBTIType is not None

def test_schema_imports():
    """Test that all Pydantic schemas can be imported"""
    assert UserCreate is not None
    assert UserLogin is not None
    assert Token is not None
    assert CelebrityCreate is not None
    assert CelebrityUpdate is not None
    assert VoteCreate is not None
    assert CommentCreate is not None

def test_mbti_types():
    """Test that all MBTI types are defined"""
    mbti_types = [
        "INTJ", "INTP", "ENTJ", "ENTP",
        "INFJ", "INFP", "ENFJ", "ENFP", 
        "ISTJ", "ISFJ", "ESTJ", "ESFJ",
        "ISTP", "ISFP", "ESTP", "ESFP"
    ]
    
    for mbti_type in mbti_types:
        assert mbti_type in [t.value for t in MBTIType]

def test_user_schema_validation():
    """Test UserCreate schema validation"""
    # Valid user data
    valid_user = UserCreate(
        email="test@example.com",
        password="password123",
        name="Test User"
    )
    assert valid_user.email == "test@example.com"
    assert valid_user.name == "Test User"
    
    # Test email validation
    with pytest.raises(ValueError):
        UserCreate(
            email="invalid-email",
            password="password123",
            name="Test User"
        )

def test_celebrity_schema_validation():
    """Test CelebrityCreate schema validation"""
    valid_celebrity = CelebrityCreate(
        name="Test Celebrity",
        description="A test celebrity",
        mbti_type="INTJ"
    )
    assert valid_celebrity.name == "Test Celebrity"
    assert valid_celebrity.mbti_type == "INTJ"

def test_vote_schema_validation():
    """Test VoteCreate schema validation"""
    valid_vote = VoteCreate(
        celebrity_id=1,
        mbti_type="INTJ",
        reason="Test reason"
    )
    assert valid_vote.celebrity_id == 1
    assert valid_vote.mbti_type == "INTJ"

def test_comment_schema_validation():
    """Test CommentCreate schema validation"""
    valid_comment = CommentCreate(
        celebrity_id=1,
        content="Test comment"
    )
    assert valid_comment.celebrity_id == 1
    assert valid_comment.content == "Test comment"

def test_file_structure():
    """Test that required files and directories exist"""
    required_files = [
        "app/main.py",
        "app/database/models.py",
        "app/schemas/auth.py",
        "app/schemas/celebrity.py",
        "app/schemas/vote.py",
        "app/schemas/comment.py",
        "requirements_minimal.txt",
        "run_local.py"
    ]
    
    for file_path in required_files:
        assert Path(file_path).exists(), f"Required file {file_path} not found"

def test_requirements_file():
    """Test that requirements file contains necessary dependencies"""
    with open("requirements_minimal.txt", "r") as f:
        requirements = f.read()
    
    required_packages = [
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "alembic",
        "python-jose",
        "passlib",
        "python-multipart",
        "jinja2"
    ]
    
    for package in required_packages:
        assert package in requirements, f"Required package {package} not found in requirements"

if __name__ == "__main__":
    pytest.main([__file__]) 