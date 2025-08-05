# 🧪 Automated Registration Tests

This directory contains automated tests for the registration process using Selenium WebDriver with Firefox browser.

## 📋 Prerequisites

### 1. Firefox Browser
- Install Firefox browser on your system
- Download from: https://www.mozilla.org/firefox/

### 2. GeckoDriver
- Download geckodriver for your platform from: https://github.com/mozilla/geckodriver/releases
- Add geckodriver to your system PATH
- Or place it in the project directory

### 3. Python Dependencies
The test runner will automatically install required dependencies:
- `selenium==4.15.2` - WebDriver automation
- `webdriver-manager==4.0.1` - Driver management
- `requests==2.31.0` - HTTP requests

## 🚀 Running Tests

### Option 1: Automatic Test Runner
```bash
python run_registration_tests.py
```

This script will:
1. ✅ Check if server is running
2. ✅ Check if Firefox is available
3. ✅ Install dependencies
4. ✅ Run all registration tests

### Option 2: Manual Test Execution
```bash
# Install dependencies
pip install selenium==4.15.2 webdriver-manager==4.0.1 requests==2.31.0

# Run tests
python test_registration_automation.py
```

## 🧪 Test Coverage

The automated tests cover:

### 1. **Homepage Loading** ✅
- Page title verification
- Navigation elements presence
- Basic page structure

### 2. **Modal Functionality** ✅
- Signup modal opens correctly
- All form fields are present
- Modal switching (login ↔ signup)

### 3. **Form Validation** ✅
- Real-time email validation
- Password length validation
- Name field validation
- Confirm password matching
- Visual feedback (red/green borders)

### 4. **Registration Flow** ✅
- Successful registration with valid data
- Duplicate email error handling
- Form loading states
- Success notifications

### 5. **Login Flow** ✅
- Login with registered account
- Authentication state verification
- Error handling for invalid credentials

### 6. **Error Handling** ✅
- Empty form submission
- Invalid input validation
- Network error simulation
- Server error responses

## 📊 Test Results

The test runner provides detailed output including:

```
🧪 Test 1: Homepage Loads
✅ Page title is correct
✅ Navigation elements are present

🧪 Test 2: Signup Modal Opens
✅ Signup modal opened
✅ All form fields are present

🧪 Test 3: Form Validation
✅ Field validation passed for signupEmail: 请输入有效的邮箱地址
✅ Field validation passed for signupPassword: 密码长度至少为6位
✅ Field validation passed for signupName: 请输入姓名
✅ Confirm password validation passed

🧪 Test 4: Successful Registration
✅ Notification check passed: 注册成功
✅ Login modal opened after successful registration

🧪 Test 5: Duplicate Email Registration
✅ Notification check passed: 该邮箱已被注册

🧪 Test 6: Login After Registration
✅ Notification check passed: 登录成功
✅ User is logged in successfully

🧪 Test 7: Form Loading States
✅ Loading state appeared
✅ Loading state completed

🧪 Test 8: Real-time Validation
✅ Real-time email validation works
✅ Real-time email success state works

🧪 Test 9: Modal Switching
✅ Switched to login modal
✅ Switched back to signup modal

🧪 Test 10: Error Handling
✅ Empty form validation works
```

## 🔧 Configuration

### Headless Mode
To run tests without opening browser windows, uncomment this line in `test_registration_automation.py`:
```python
firefox_options.add_argument("--headless")
```

### Custom Test Data
Modify test data in the `setUp` method:
```python
self.test_email = f"test_{self._generate_random_string(8)}@example.com"
self.test_password = "testpassword123"
self.test_name = f"Test User {self._generate_random_string(5)}"
```

### Timeout Settings
Adjust timeouts for slower systems:
```python
self.driver.implicitly_wait(10)  # Default wait
self.wait = WebDriverWait(self.driver, 10)  # Explicit wait
```

## 🐛 Troubleshooting

### Firefox Not Found
```
❌ Firefox WebDriver not available
```
**Solution**: Install Firefox browser and geckodriver

### Server Not Running
```
❌ Server is not running
```
**Solution**: Start the server with `python run_local.py`

### Element Not Found
```
❌ Element not found: signupBtn
```
**Solution**: Check if the page loaded correctly and elements exist

### Test Failures
- Check browser console for JavaScript errors
- Verify server is responding correctly
- Check network connectivity
- Review test logs for specific failure reasons

## 📈 Performance

- **Test Duration**: ~2-3 minutes for full suite
- **Browser Memory**: ~100-200MB per test
- **Network Usage**: Minimal (local server)
- **CPU Usage**: Low to moderate

## 🔄 Continuous Integration

For CI/CD integration, the tests can be run with:
```bash
# Install dependencies
pip install -r requirements_test.txt

# Run tests with headless mode
python test_registration_automation.py
```

## 📝 Adding New Tests

To add new test cases:

1. Add new test method to `RegistrationAutomationTest` class
2. Follow naming convention: `test_XX_description`
3. Use helper methods for common operations
4. Add proper assertions and error handling
5. Update this README with new test coverage

Example:
```python
def test_11_new_feature(self):
    """Test new registration feature"""
    print("\n🧪 Test 11: New Feature")
    # Test implementation
    self.assertTrue(condition, "Expected behavior")
    print("✅ New feature test passed")
``` 