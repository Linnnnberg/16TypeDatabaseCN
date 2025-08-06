"""
Basic pytest tests for MBTI Roster
These tests can run in CI environment without requiring a running server
"""

import pytest
import sys
import os
from pathlib import Path


def test_python_version():
    """Test that Python is working"""
    assert sys.version_info >= (3, 8)


def test_working_directory():
    """Test that we're in the right directory"""
    assert os.path.exists("requirements_minimal.txt")


def test_requirements_file():
    """Test that requirements file exists and has content"""
    with open("requirements_minimal.txt", "r") as f:
        content = f.read()
        assert "fastapi" in content
        assert "uvicorn" in content


def test_app_structure():
    """Test that basic app structure exists"""
    assert os.path.exists("app")
    assert os.path.exists("app/main.py")
    assert os.path.exists("app/database/models.py")


def test_templates_exist():
    """Test that templates exist"""
    assert os.path.exists("templates")
    assert os.path.exists("templates/base.html")


def test_static_files_exist():
    """Test that static files exist"""
    assert os.path.exists("static")
    assert os.path.exists("static/css/style.css")
    assert os.path.exists("static/js/main.js")


def test_mbti_types_list():
    """Test that MBTI types are properly defined"""
    mbti_types = [
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
    ]

    assert len(mbti_types) == 16
    assert "INTJ" in mbti_types
    assert "ESFP" in mbti_types


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
        "run_local.py",
    ]

    for file_path in required_files:
        assert Path(file_path).exists(), f"Required file {file_path} not found"


def test_requirements_file_content():
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
        "jinja2",
    ]

    for package in required_packages:
        assert (
            package in requirements
        ), f"Required package {package} not found in requirements"


def test_app_imports():
    """Test that app modules can be imported without errors"""
    try:
        # Test core imports
        from app.core.config import settings

        assert settings is not None

        # Test database imports
        from app.database.models import Base, User, Celebrity, Vote, Comment

        assert Base is not None
        assert User is not None
        assert Celebrity is not None
        assert Vote is not None
        assert Comment is not None

        # Test schema imports
        from app.schemas.auth import UserCreate, UserLogin, UserResponse

        assert UserCreate is not None
        assert UserLogin is not None
        assert UserResponse is not None

        from app.schemas.celebrity import CelebrityCreate, CelebrityResponse

        assert CelebrityCreate is not None
        assert CelebrityResponse is not None

        from app.schemas.vote import VoteCreate, VoteResponse

        assert VoteCreate is not None
        assert VoteResponse is not None

        # Test service imports
        from app.services.auth_service import AuthService
        from app.services.user_service import UserService

        assert AuthService is not None
        assert UserService is not None

    except ImportError as e:
        pytest.fail(f"Failed to import app modules: {e}")


def test_config_loading():
    """Test that configuration loads correctly"""
    try:
        from app.core.config import settings

        # Test that required settings are available
        assert hasattr(settings, "database_url")
        assert hasattr(settings, "secret_key")
        assert hasattr(settings, "redis_url")
        assert hasattr(settings, "email_from")

        # Test that secret_key has a value (should have default)
        assert settings.secret_key is not None
        assert len(settings.secret_key) > 0

    except Exception as e:
        pytest.fail(f"Failed to load configuration: {e}")


def test_database_models():
    """Test that database models can be defined"""
    try:
        from app.database.models import User, Celebrity, Vote, Comment

        # Test that models have required attributes
        assert hasattr(User, "__tablename__")
        assert hasattr(Celebrity, "__tablename__")
        assert hasattr(Vote, "__tablename__")
        assert hasattr(Comment, "__tablename__")

        # Test that tablenames are defined
        assert User.__tablename__ == "users"
        assert Celebrity.__tablename__ == "celebrities"
        assert Vote.__tablename__ == "votes"
        assert Comment.__tablename__ == "comments"

    except Exception as e:
        pytest.fail(f"Failed to test database models: {e}")


def test_schema_validation():
    """Test that Pydantic schemas work correctly"""
    try:
        from app.schemas.auth import UserCreate, UserLogin

        # Test UserCreate schema
        user_data = {
            "email": "test@example.com",
            "password": "testpassword123",
            "name": "Test User",
        }
        user_create = UserCreate(**user_data)
        assert user_create.email == "test@example.com"
        assert user_create.name == "Test User"

        # Test UserLogin schema
        login_data = {"email": "test@example.com", "password": "testpassword123"}
        user_login = UserLogin(**login_data)
        assert user_login.email == "test@example.com"

    except Exception as e:
        pytest.fail(f"Failed to test schema validation: {e}")


def test_security_functions():
    """Test that security functions can be imported and used"""
    try:
        from app.core.security import (
            create_access_token,
            verify_password,
            get_password_hash,
        )

        # Test password hashing
        password = "testpassword123"
        hashed = get_password_hash(password)
        assert hashed != password
        assert verify_password(password, hashed)
        assert not verify_password("wrongpassword", hashed)

        # Test token creation (basic test)
        token_data = {"sub": "test@example.com"}
        token = create_access_token(token_data)
        assert token is not None
        assert len(token) > 0

    except Exception as e:
        pytest.fail(f"Failed to test security functions: {e}")


if __name__ == "__main__":
    pytest.main([__file__])
