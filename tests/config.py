"""
Test configuration and utilities for MBTI Roster regression tests
"""
import os
import sys
import json
import requests
from typing import Dict, Any, Optional
from datetime import datetime

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

class TestConfig:
    """Test configuration and utilities"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.admin_credentials = {
            "email": "admin@mbti-roster.com",
            "password": "admin123"
        }
        self.test_user_credentials = {
            "email": "test@mbti-roster.com",
            "password": "test123"
        }
        self.auth_token = None
        self.test_results = []
        
    def get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers for API requests"""
        if self.auth_token:
            return {"Authorization": f"Bearer {self.auth_token}"}
        return {}
    
    def login_admin(self) -> bool:
        """Login as admin user and store token"""
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                json=self.admin_credentials
            )
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get("access_token")
                return True
            return False
        except Exception as e:
            print(f"Login failed: {e}")
            return False
    
    def make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make authenticated API request"""
        url = f"{self.base_url}{endpoint}"
        headers = self.get_auth_headers()
        
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
            del kwargs['headers']
        
        return requests.request(method, url, headers=headers, **kwargs)
    
    def add_test_result(self, test_name: str, success: bool, details: str = ""):
        """Add test result to the collection"""
        self.test_results.append({
            "test_name": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_test_summary(self) -> Dict[str, Any]:
        """Get summary of all test results"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "results": self.test_results
        }
    
    def save_test_report(self, filename: str = None):
        """Save test results to a JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_report_{timestamp}.json"
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": self.get_test_summary(),
            "config": {
                "base_url": self.base_url,
                "admin_email": self.admin_credentials["email"]
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"Test report saved to: {filename}")
        return filename

# Global test configuration instance
test_config = TestConfig() 