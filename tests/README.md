# MBTI Roster Regression Testing Framework

## Overview

This testing framework provides comprehensive regression testing for the MBTI Roster application. It's designed to ensure that all features continue to work correctly as new features are added or existing code is modified.

## 🏗️ Architecture

### Directory Structure
```
tests/
├── __init__.py              # Package initialization
├── config.py                # Test configuration and utilities
├── test_auth.py            # Authentication system tests
├── test_celebrities.py     # Celebrity management tests
├── test_voting.py          # Voting system tests
├── test_comments.py        # Comment system tests
├── test_search.py          # Search functionality tests
├── run_all_tests.py        # Main test orchestrator
└── README.md               # This documentation
```

### Test Reports
```
test_reports/
└── regression_test_report_YYYYMMDD_HHMMSS.json
```

## 🚀 Quick Start

### Prerequisites
1. Ensure the server is running: `python run_local.py`
2. Make sure you have the `requests` library installed: `pip install requests`

### Running Tests

#### Run All Tests
```bash
python run_tests.py
```

#### Run Specific Test Suite
```bash
python run_tests.py auth          # Authentication tests only
python run_tests.py celebrities   # Celebrity management tests only
python run_tests.py voting        # Voting system tests only
python run_tests.py comments      # Comment system tests only
python run_tests.py search        # Search functionality tests only
```

#### Run Individual Test Files
```bash
python -m tests.test_auth
python -m tests.test_celebrities
python -m tests.test_voting
python -m tests.test_comments
python -m tests.test_search
```

## 📋 Test Suites

### 1. Authentication System (`test_auth.py`)
- **Health Check**: Basic server connectivity
- **Admin Login**: Admin user authentication
- **Get Current User**: Profile retrieval
- **User Registration**: New user creation
- **Invalid Login**: Error handling for invalid credentials

### 2. Celebrity Management (`test_celebrities.py`)
- **Get All Celebrities**: List all celebrities
- **Get Celebrity by ID**: Retrieve specific celebrity
- **Search Celebrities**: Search functionality
- **Get Popular Celebrities**: Popular celebrities list
- **Get Celebrities by Tag**: Filter by tags
- **Create Celebrity**: Admin-only creation
- **Update Celebrity**: Admin-only updates
- **Add Tag to Celebrity**: Tag management

### 3. Voting System (`test_voting.py`)
- **Get MBTI Types**: All 16 MBTI types
- **Get All Votes**: List all votes
- **Create Vote**: Vote creation with validation
- **Get User Votes**: User-specific votes
- **Get Celebrity Votes**: Celebrity-specific votes
- **Get Vote Statistics**: Vote analytics
- **Delete Vote**: Vote deletion
- **Duplicate Vote Validation**: Prevent duplicate votes

### 4. Comment System (`test_comments.py`)
- **Get All Comments**: List all comments
- **Create Comment**: Comment creation
- **Get User Comments**: User-specific comments
- **Get Celebrity Comments**: Celebrity-specific comments
- **Create Reply**: Nested comment replies
- **Update Comment**: Comment editing
- **Delete Comment**: Comment deletion
- **Get Comment Statistics**: Comment analytics

### 5. Search Functionality (`test_search.py`)
- **Basic Search**: Hybrid search functionality
- **Search by Name**: Name-specific search
- **Search by Description**: Description search
- **Search by Tag**: Tag-based search
- **Search by MBTI**: MBTI type search
- **Search with Filters**: Combined filters
- **Search Suggestions**: Autocomplete
- **Search Analytics**: Search statistics
- **MBTI Types Endpoint**: Available types
- **Popular Searches**: Trending searches
- **Search Pagination**: Pagination support
- **Empty Search Query**: Error handling

## 🔧 Configuration

### Test Configuration (`config.py`)
The test configuration is centralized in `tests/config.py`:

```python
class TestConfig:
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
```

### Customizing Test Settings
You can modify the configuration by editing `tests/config.py`:
- Change `base_url` for different environments
- Update credentials for different test users
- Modify timeout settings
- Add custom test data

## 📊 Test Reports

### Report Structure
Each test run generates a detailed JSON report with:
- **Timestamp**: When the test was run
- **Summary**: Overall test statistics
- **Individual Results**: Detailed results for each test
- **Configuration**: Test environment settings

### Report Location
Reports are saved in `test_reports/` directory with timestamped filenames:
```
test_reports/regression_test_report_20240805_143022.json
```

### Report Content
```json
{
  "timestamp": "2024-08-05T14:30:22",
  "summary": {
    "total_tests": 45,
    "passed_tests": 43,
    "failed_tests": 2,
    "success_rate": 95.6
  },
  "results": [
    {
      "test_name": "Health Check",
      "success": true,
      "details": "Status: 200, Response: {...}",
      "timestamp": "2024-08-05T14:30:22"
    }
  ],
  "config": {
    "base_url": "http://localhost:8000",
    "admin_email": "admin@mbti-roster.com"
  }
}
```

## 🛠️ Adding New Tests

### 1. Create New Test File
Create a new file in the `tests/` directory:
```python
# tests/test_new_feature.py
import requests
from tests.config import test_config

def test_new_feature():
    """Test new feature functionality"""
    try:
        response = test_config.make_request("GET", "/new-feature/")
        success = response.status_code == 200
        test_config.add_test_result(
            "New Feature Test",
            success,
            f"Status: {response.status_code}"
        )
        return success
    except Exception as e:
        test_config.add_test_result("New Feature Test", False, str(e))
        return False

def run_new_feature_tests():
    """Run all new feature tests"""
    print("🆕 Running New Feature Tests...")
    
    tests = [test_new_feature]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"✅ New Feature Tests: {passed}/{total} passed")
    return passed == total

if __name__ == "__main__":
    run_new_feature_tests()
```

### 2. Add to Main Test Runner
Update `tests/run_all_tests.py`:
```python
from tests.test_new_feature import run_new_feature_tests

# Add to test_suites list:
test_suites = [
    # ... existing suites ...
    ("New Feature", run_new_feature_tests)
]
```

### 3. Add to Simple Runner
Update `run_tests.py`:
```python
elif test_suite == "new-feature":
    from tests.test_new_feature import run_new_feature_tests
    run_new_feature_tests()
```

## 🔍 Best Practices

### 1. Test Independence
- Each test should be independent
- Tests should not rely on the state from other tests
- Use fresh data for each test when possible

### 2. Error Handling
- Always wrap test logic in try-catch blocks
- Provide meaningful error messages
- Log detailed information for debugging

### 3. Test Data
- Use realistic test data
- Avoid hardcoded IDs when possible
- Clean up test data after tests

### 4. Performance
- Keep tests fast and efficient
- Avoid unnecessary API calls
- Use appropriate timeouts

## 🚨 Troubleshooting

### Common Issues

#### 1. Server Not Running
```
❌ Cannot connect to server: Connection refused
💡 Make sure the server is running with: python run_local.py
```

#### 2. Authentication Failed
```
❌ Admin login failed
💡 Check admin credentials in tests/config.py
```

#### 3. Test Dependencies
```
❌ ImportError: No module named 'tests'
💡 Run tests from project root directory
```

### Debug Mode
For detailed debugging, you can modify test functions to print more information:
```python
def test_debug_example():
    try:
        print(f"Making request to: {test_config.base_url}/endpoint")
        response = test_config.make_request("GET", "/endpoint")
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        # ... rest of test
    except Exception as e:
        print(f"Exception details: {e}")
        # ... error handling
```

## 📈 Continuous Integration

### GitHub Actions Example
```yaml
name: Regression Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Start server
        run: python run_local.py &
      - name: Wait for server
        run: sleep 10
      - name: Run tests
        run: python run_tests.py
```

## 📝 Maintenance

### Regular Tasks
1. **Update test data** when API changes
2. **Add new tests** for new features
3. **Review failed tests** and fix issues
4. **Clean up old reports** periodically
5. **Update documentation** when needed

### Test Maintenance Checklist
- [ ] All tests pass consistently
- [ ] Test data is up to date
- [ ] New features have tests
- [ ] Documentation is current
- [ ] Reports are being generated
- [ ] CI/CD integration is working

---

**🎯 Goal**: Ensure the MBTI Roster application remains stable and functional as it evolves. 