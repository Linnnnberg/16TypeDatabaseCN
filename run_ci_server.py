#!/usr/bin/env python3
"""
CI Server Startup Script
Simplified server startup for CI/CD environments
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def setup_ci_environment():
    """Set up environment variables for CI"""
    print("Setting up CI environment...")
    
    # Set environment variables for CI BEFORE importing app
    os.environ["CI"] = "true"
    os.environ["DATABASE_URL"] = "sqlite:///./test_mbti_roster.db"
    os.environ["SECRET_KEY"] = "test-secret-key-for-ci-12345"
    os.environ["REDIS_URL"] = "redis://localhost:6379"
    os.environ["EMAIL_FROM"] = "noreply@mbti-roster.local"
    os.environ["DAILY_VOTE_LIMIT"] = "20"
    os.environ["DAILY_NO_REASON_LIMIT"] = "5"
    os.environ["NEW_USER_24H_LIMIT"] = "3"
    os.environ["DAILY_REGISTRATIONS_PER_IP"] = "3"
    
    print("CI environment setup complete")

def wait_for_server(url: str, max_attempts: int = 30, delay: int = 2):
    """Wait for server to be ready"""
    print(f"Waiting for server at {url}...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"Server is ready! (attempt {attempt + 1})")
                return True
        except requests.exceptions.RequestException:
            pass
        
        print(f"Waiting for server... (attempt {attempt + 1}/{max_attempts})")
        time.sleep(delay)
    
    print("Server failed to start within expected time")
    return False

def start_server():
    """Start the FastAPI server"""
    print("Starting FastAPI server...")
    print("Server URL: http://localhost:8000")
    print("Health check: http://localhost:8000/health")
    print("API docs: http://localhost:8000/docs")
    
    try:
        # Start server in background
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ])
        
        # Wait for server to be ready
        if wait_for_server("http://localhost:8000/health"):
            print("Server started successfully!")
            return process
        else:
            print("Failed to start server")
            process.terminate()
            return None
            
    except Exception as e:
        print(f"Error starting server: {e}")
        return None

def main():
    """Main function"""
    print("=== MBTI Roster - CI Server Startup ===")
    
    # Setup environment BEFORE any app imports
    setup_ci_environment()
    
    # Start server
    process = start_server()
    
    if process:
        try:
            # Keep server running
            process.wait()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            process.terminate()
            process.wait()
    else:
        sys.exit(1)

if __name__ == "__main__":
    main() 