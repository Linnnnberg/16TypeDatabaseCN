#!/usr/bin/env python3
"""
Development Setup Script for 16型花名册 (MBTI Roster)
Handles all common development tasks in one place
"""

import os
import sys
import subprocess
import time
import json
import requests
from pathlib import Path

class DevSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.venv_python = self.project_root / "venv" / "Scripts" / "python.exe"
        self.venv_uvicorn = self.project_root / "venv" / "Scripts" / "uvicorn.exe"
        self.server_url = "http://localhost:8000"
        
    def run_command(self, command, description="", check=True):
        """Run a command and handle output"""
        print(f"\n🔄 {description}")
        print(f"   Running: {command}")
        
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                print(f"   ✅ Success")
                if result.stdout.strip():
                    print(f"   Output: {result.stdout.strip()}")
            else:
                print(f"   ❌ Failed")
                if result.stderr.strip():
                    print(f"   Error: {result.stderr.strip()}")
                if check:
                    raise Exception(f"Command failed: {command}")
            
            return result
        except Exception as e:
            print(f"   ❌ Exception: {e}")
            if check:
                raise
            return None
    
    def check_venv(self):
        """Check if virtual environment exists"""
        if not self.venv_python.exists():
            print("❌ Virtual environment not found!")
            print("   Please run: python -m venv venv")
            return False
        return True
    
    def setup_environment(self):
        """Setup environment variables"""
        print("\n🔧 Setting up environment...")
        
        env_file = self.project_root / ".env"
        if not env_file.exists():
            print("   Creating .env file...")
            env_content = """DATABASE_URL=sqlite:///./mbti_roster.db
SECRET_KEY=your-super-secret-key-here-change-in-production
REDIS_URL=redis://localhost:6379
EMAIL_FROM=noreply@mbti-roster.com"""
            
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(env_content)
            print("   ✅ .env file created")
        else:
            print("   ✅ .env file already exists")
    
    def install_dependencies(self):
        """Install Python dependencies"""
        print("\n📦 Installing dependencies...")
        
        # Check if requirements file exists
        requirements_file = self.project_root / "requirements_minimal.txt"
        if not requirements_file.exists():
            print("   ❌ requirements_minimal.txt not found!")
            return False
        
        # Install dependencies
        self.run_command(
            f'"{self.venv_python}" -m pip install -r requirements_minimal.txt',
            "Installing Python dependencies"
        )
        return True
    
    def create_admin_user(self):
        """Create admin user if not exists"""
        print("\n👤 Setting up admin user...")
        
        admin_script = self.project_root / "create_admin.py"
        if admin_script.exists():
            self.run_command(
                f'"{self.venv_python}" create_admin.py',
                "Creating admin user",
                check=False
            )
        else:
            print("   ⚠️  create_admin.py not found, skipping admin creation")
    
    def create_sample_data(self):
        """Create sample celebrities and votes"""
        print("\n🎭 Creating sample data...")
        
        # Create celebrities
        celeb_script = self.project_root / "create_sample_celebrities.py"
        if celeb_script.exists():
            self.run_command(
                f'"{self.venv_python}" create_sample_celebrities.py',
                "Creating sample celebrities",
                check=False
            )
        else:
            print("   ⚠️  create_sample_celebrities.py not found")
        
        # Create votes
        vote_script = self.project_root / "create_sample_votes.py"
        if vote_script.exists():
            self.run_command(
                f'"{self.venv_python}" create_sample_votes.py',
                "Creating sample votes",
                check=False
            )
        else:
            print("   ⚠️  create_sample_votes.py not found")
    
    def start_server(self, background=True):
        """Start the FastAPI server"""
        print("\n🚀 Starting FastAPI server...")
        
        if background:
            # Start server in background
            try:
                process = subprocess.Popen(
                    [str(self.venv_uvicorn), "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
                    cwd=self.project_root,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                
                # Wait a bit for server to start
                time.sleep(3)
                
                # Check if server is running
                if self.check_server():
                    print("   ✅ Server started successfully")
                    return process
                else:
                    print("   ❌ Server failed to start")
                    return None
                    
            except Exception as e:
                print(f"   ❌ Failed to start server: {e}")
                return None
        else:
            # Start server in foreground (blocking)
            self.run_command(
                f'"{self.venv_uvicorn}" app.main:app --host 0.0.0.0 --port 8000 --reload',
                "Starting server (foreground)",
                check=False
            )
    
    def check_server(self):
        """Check if server is running"""
        try:
            response = requests.get(f"{self.server_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def test_endpoints(self):
        """Test basic endpoints"""
        print("\n🧪 Testing endpoints...")
        
        if not self.check_server():
            print("   ❌ Server not running, skipping tests")
            return
        
        endpoints = [
            ("/health", "Health check"),
            ("/", "Root endpoint"),
            ("/test", "Test endpoint"),
            ("/celebrities/", "Celebrities list"),
            ("/votes/mbti-types", "MBTI types"),
        ]
        
        for endpoint, description in endpoints:
            try:
                response = requests.get(f"{self.server_url}{endpoint}", timeout=5)
                status = "✅" if response.status_code == 200 else "❌"
                print(f"   {status} {description}: {response.status_code}")
            except Exception as e:
                print(f"   ❌ {description}: Error - {e}")
    
    def show_info(self):
        """Show development information"""
        print("\n📋 Development Information")
        print("=" * 50)
        print(f"🌐 Server URL: {self.server_url}")
        print(f"📚 API Docs: {self.server_url}/docs")
        print(f"🔍 Health Check: {self.server_url}/health")
        print(f"🧪 Test Endpoint: {self.server_url}/test")
        print("\n🔑 Admin Credentials:")
        print("   Email: admin@mbti-roster.com")
        print("   Password: admin123")
        print("\n📝 Available Endpoints:")
        print("   Authentication:")
        print("     POST /auth/signup - Register user")
        print("     POST /auth/login - Login user")
        print("     GET /auth/me - Get current user")
        print("   Celebrities:")
        print("     GET /celebrities/ - List celebrities")
        print("     POST /celebrities/ - Create celebrity (admin)")
        print("     GET /celebrities/popular - Popular celebrities")
        print("   Votes:")
        print("     POST /votes/ - Create vote")
        print("     GET /votes/ - List votes")
        print("     GET /votes/my-votes - My votes")
        print("     GET /votes/statistics/celebrity/{id} - Celebrity stats")
        print("     GET /votes/statistics/my-stats - My stats")
        print("\n🛠️  Development Commands:")
        print("   python dev_setup.py --full - Full setup")
        print("   python dev_setup.py --server - Start server only")
        print("   python dev_setup.py --test - Test endpoints only")
        print("   python dev_setup.py --data - Create sample data only")
    
    def full_setup(self):
        """Run full development setup"""
        print("🎯 16型花名册 (MBTI Roster) - Development Setup")
        print("=" * 60)
        
        # Check virtual environment
        if not self.check_venv():
            return False
        
        # Setup environment
        self.setup_environment()
        
        # Install dependencies
        if not self.install_dependencies():
            return False
        
        # Create admin user
        self.create_admin_user()
        
        # Create sample data
        self.create_sample_data()
        
        # Start server
        server_process = self.start_server(background=True)
        
        # Test endpoints
        self.test_endpoints()
        
        # Show information
        self.show_info()
        
        print("\n🎉 Development setup complete!")
        print("   Press Ctrl+C to stop the server")
        
        # Keep server running
        try:
            if server_process:
                server_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping server...")
            if server_process:
                server_process.terminate()
        
        return True

def main():
    """Main function"""
    setup = DevSetup()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--full":
            setup.full_setup()
        elif command == "--server":
            setup.start_server(background=False)
        elif command == "--test":
            setup.test_endpoints()
        elif command == "--data":
            setup.create_sample_data()
        elif command == "--info":
            setup.show_info()
        else:
            print(f"❌ Unknown command: {command}")
            print("Available commands: --full, --server, --test, --data, --info")
    else:
        # Default: full setup
        setup.full_setup()

if __name__ == "__main__":
    main() 