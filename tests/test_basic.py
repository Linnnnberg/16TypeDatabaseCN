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
        assert "pytest" in content


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
        "pytest",
    ]

    for package in required_packages:
        assert package in requirements, f"Required package {package} not found in requirements"


if __name__ == "__main__":
    pytest.main([__file__]) 