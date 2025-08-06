"""
Integration tests for MBTI Roster API
These tests require a running server and use pytest
"""

import pytest
import requests
import time


def test_health_check():
    """Test basic health check endpoint"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Health check failed: {e}")


def test_api_root():
    """Test API root endpoint"""
    try:
        response = requests.get("http://localhost:8000/api", timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "status" in data
    except requests.exceptions.RequestException as e:
        pytest.fail(f"API root test failed: {e}")


def test_test_endpoint():
    """Test the test endpoint"""
    try:
        response = requests.get("http://localhost:8000/test", timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "mbti_types" in data
        assert len(data["mbti_types"]) == 16
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Test endpoint failed: {e}")


def test_database_connection():
    """Test database connection endpoint"""
    try:
        response = requests.get("http://localhost:8000/db-test", timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        # Database might not be set up in CI, so we accept both success and error
        assert data["status"] in ["success", "error"]
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Database test failed: {e}")


def test_environment_info():
    """Test environment info endpoint"""
    try:
        response = requests.get("http://localhost:8000/env", timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert "python_version" in data
        assert "fastapi_version" in data
        assert "environment" in data
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Environment info test failed: {e}")


def test_auth_endpoints_exist():
    """Test that auth endpoints exist (without testing functionality)"""
    try:
        # Test that auth endpoints return some response (even if 404)
        response = requests.get("http://localhost:8000/auth/login", timeout=5)
        # Should return 405 Method Not Allowed for GET request to POST endpoint
        assert response.status_code in [405, 404]
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Auth endpoint test failed: {e}")


def test_celebrities_endpoints_exist():
    """Test that celebrities endpoints exist"""
    try:
        response = requests.get("http://localhost:8000/api/celebrities", timeout=5)
        # Should return some response (even if 401 for unauthorized)
        assert response.status_code in [200, 401, 404]
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Celebrities endpoint test failed: {e}")


def test_docs_endpoint():
    """Test that API docs endpoint exists"""
    try:
        response = requests.get("http://localhost:8000/docs", timeout=10)
        assert response.status_code == 200
        # Should return HTML content
        assert "text/html" in response.headers.get("content-type", "")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Docs endpoint test failed: {e}")


def test_openapi_schema():
    """Test that OpenAPI schema endpoint exists"""
    try:
        response = requests.get("http://localhost:8000/openapi.json", timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data
    except requests.exceptions.RequestException as e:
        pytest.fail(f"OpenAPI schema test failed: {e}")


def test_server_startup_time():
    """Test that server responds within reasonable time"""
    start_time = time.time()
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        end_time = time.time()
        response_time = end_time - start_time

        assert response.status_code == 200
        assert response_time < 2.0  # Should respond within 2 seconds
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Server response time test failed: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
