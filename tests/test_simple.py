"""
Simple test file that should work in CI environment
"""
import os
import sys
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

if __name__ == "__main__":
    # Simple test runner
    tests = [
        test_python_version,
        test_working_directory,
        test_requirements_file,
        test_app_structure,
        test_templates_exist,
        test_static_files_exist
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            print(f"✅ {test.__name__} passed")
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")
    if failed > 0:
        sys.exit(1) 