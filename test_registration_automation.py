#!/usr/bin/env python3
"""
Automated Registration Process Test
Tests the complete registration flow using Selenium WebDriver with Firefox browser
"""

import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import random
import string

class RegistrationAutomationTest(unittest.TestCase):
    """Automated test suite for registration process"""
    
    def setUp(self):
        """Set up Firefox WebDriver with options"""
        # Configure Firefox options
        firefox_options = Options()
        firefox_options.add_argument("--width=1920")
        firefox_options.add_argument("--height=1080")
        # firefox_options.add_argument("--headless")  # Uncomment for headless mode
        
        # Initialize WebDriver
        self.driver = webdriver.Firefox(options=firefox_options)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)
        
        # Test data
        self.base_url = "http://localhost:8000"
        self.test_email = f"test_{self._generate_random_string(8)}@example.com"
        self.test_password = "testpassword123"
        self.test_name = f"Test User {self._generate_random_string(5)}"
    
    def tearDown(self):
        """Clean up WebDriver"""
        if hasattr(self, 'driver'):
            self.driver.quit()
    
    def _generate_random_string(self, length):
        """Generate random string for test data"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    
    def _wait_for_element(self, by, value, timeout=10):
        """Wait for element to be present and visible"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
    
    def _wait_for_element_clickable(self, by, value, timeout=10):
        """Wait for element to be clickable"""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
    
    def _check_notification(self, expected_text, notification_type="success"):
        """Check if notification appears with expected text"""
        try:
            notification = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "fixed"))
            )
            self.assertIn(expected_text, notification.text)
            print(f"✅ Notification check passed: {expected_text}")
            return True
        except TimeoutException:
            print(f"❌ Notification not found: {expected_text}")
            return False
    
    def _check_field_validation(self, field_id, invalid_value, expected_error):
        """Test field validation with invalid input"""
        field = self.driver.find_element(By.ID, field_id)
        field.clear()
        field.send_keys(invalid_value)
        field.send_keys("\t")  # Trigger blur event
        
        # Wait for error message
        try:
            error_div = self.driver.find_element(By.ID, f"{field_id}Error")
            self.assertIn(expected_error, error_div.text)
            print(f"✅ Field validation passed for {field_id}: {expected_error}")
            return True
        except NoSuchElementException:
            print(f"❌ Field validation failed for {field_id}")
            return False
    
    def test_01_homepage_loads(self):
        """Test that homepage loads correctly"""
        print("\n🧪 Test 1: Homepage Loads")
        self.driver.get(self.base_url)
        
        # Check page title
        self.assertIn("16型花名册", self.driver.title)
        print("✅ Page title is correct")
        
        # Check navigation elements
        nav_elements = ["首页", "名人库", "MBTI测试", "关于MBTI", "登录", "注册"]
        for element_text in nav_elements:
            element = self.driver.find_element(By.XPATH, f"//*[contains(text(), '{element_text}')]")
            self.assertTrue(element.is_displayed())
        print("✅ Navigation elements are present")
    
    def test_02_signup_modal_opens(self):
        """Test that signup modal opens correctly"""
        print("\n🧪 Test 2: Signup Modal Opens")
        self.driver.get(self.base_url)
        
        # Click signup button
        signup_btn = self._wait_for_element_clickable(By.ID, "signupBtn")
        signup_btn.click()
        
        # Check modal is visible
        modal = self._wait_for_element(By.ID, "signupModal")
        self.assertTrue(modal.is_displayed())
        print("✅ Signup modal opened")
        
        # Check form fields are present
        required_fields = ["signupName", "signupEmail", "signupPassword", "signupConfirmPassword"]
        for field_id in required_fields:
            field = self.driver.find_element(By.ID, field_id)
            self.assertTrue(field.is_displayed())
        print("✅ All form fields are present")
    
    def test_03_form_validation(self):
        """Test form validation with invalid inputs"""
        print("\n🧪 Test 3: Form Validation")
        self.driver.get(self.base_url)
        
        # Open signup modal
        signup_btn = self._wait_for_element_clickable(By.ID, "signupBtn")
        signup_btn.click()
        
        # Test email validation
        self._check_field_validation("signupEmail", "invalid-email", "请输入有效的邮箱地址")
        
        # Test password validation
        self._check_field_validation("signupPassword", "123", "密码长度至少为6位")
        
        # Test name validation
        self._check_field_validation("signupName", "", "请输入姓名")
        
        # Test confirm password validation
        email_field = self.driver.find_element(By.ID, "signupEmail")
        email_field.clear()
        email_field.send_keys("test@example.com")
        
        password_field = self.driver.find_element(By.ID, "signupPassword")
        password_field.clear()
        password_field.send_keys("password123")
        
        confirm_field = self.driver.find_element(By.ID, "signupConfirmPassword")
        confirm_field.clear()
        confirm_field.send_keys("different")
        confirm_field.send_keys("\t")
        
        try:
            error_div = self.driver.find_element(By.ID, "signupConfirmPasswordError")
            self.assertIn("两次输入的密码不一致", error_div.text)
            print("✅ Confirm password validation passed")
        except NoSuchElementException:
            print("❌ Confirm password validation failed")
    
    def test_04_successful_registration(self):
        """Test successful registration flow"""
        print("\n🧪 Test 4: Successful Registration")
        self.driver.get(self.base_url)
        
        # Open signup modal
        signup_btn = self._wait_for_element_clickable(By.ID, "signupBtn")
        signup_btn.click()
        
        # Fill form with valid data
        name_field = self.driver.find_element(By.ID, "signupName")
        name_field.clear()
        name_field.send_keys(self.test_name)
        
        email_field = self.driver.find_element(By.ID, "signupEmail")
        email_field.clear()
        email_field.send_keys(self.test_email)
        
        password_field = self.driver.find_element(By.ID, "signupPassword")
        password_field.clear()
        password_field.send_keys(self.test_password)
        
        confirm_field = self.driver.find_element(By.ID, "signupConfirmPassword")
        confirm_field.clear()
        confirm_field.send_keys(self.test_password)
        
        # Submit form
        submit_btn = self.driver.find_element(By.XPATH, "//form[@id='signupForm']//button[@type='submit']")
        submit_btn.click()
        
        # Check for success notification
        success = self._check_notification("注册成功", "success")
        self.assertTrue(success, "Registration should succeed")
        
        # Check that login modal opens
        try:
            login_modal = self._wait_for_element(By.ID, "loginModal")
            self.assertTrue(login_modal.is_displayed())
            print("✅ Login modal opened after successful registration")
        except TimeoutException:
            print("❌ Login modal did not open after registration")
    
    def test_05_duplicate_email_registration(self):
        """Test registration with duplicate email"""
        print("\n🧪 Test 5: Duplicate Email Registration")
        self.driver.get(self.base_url)
        
        # Open signup modal
        signup_btn = self._wait_for_element_clickable(By.ID, "signupBtn")
        signup_btn.click()
        
        # Fill form with existing email
        name_field = self.driver.find_element(By.ID, "signupName")
        name_field.clear()
        name_field.send_keys("Duplicate User")
        
        email_field = self.driver.find_element(By.ID, "signupEmail")
        email_field.clear()
        email_field.send_keys(self.test_email)  # Use the email from previous test
        
        password_field = self.driver.find_element(By.ID, "signupPassword")
        password_field.clear()
        password_field.send_keys("password123")
        
        confirm_field = self.driver.find_element(By.ID, "signupConfirmPassword")
        confirm_field.clear()
        confirm_field.send_keys("password123")
        
        # Submit form
        submit_btn = self.driver.find_element(By.XPATH, "//form[@id='signupForm']//button[@type='submit']")
        submit_btn.click()
        
        # Check for error notification
        error = self._check_notification("该邮箱已被注册", "error")
        self.assertTrue(error, "Should show duplicate email error")
    
    def test_06_login_after_registration(self):
        """Test login with newly registered account"""
        print("\n🧪 Test 6: Login After Registration")
        self.driver.get(self.base_url)
        
        # Open login modal
        login_btn = self._wait_for_element_clickable(By.ID, "loginBtn")
        login_btn.click()
        
        # Fill login form
        email_field = self.driver.find_element(By.ID, "loginEmail")
        email_field.clear()
        email_field.send_keys(self.test_email)
        
        password_field = self.driver.find_element(By.ID, "loginPassword")
        password_field.clear()
        password_field.send_keys(self.test_password)
        
        # Submit login form
        submit_btn = self.driver.find_element(By.XPATH, "//form[@id='loginForm']//button[@type='submit']")
        submit_btn.click()
        
        # Check for success notification
        success = self._check_notification("登录成功", "success")
        self.assertTrue(success, "Login should succeed")
        
        # Check that user is logged in (button text should change)
        try:
            login_btn = self.driver.find_element(By.ID, "loginBtn")
            self.assertEqual(login_btn.text, self.test_email)
            print("✅ User is logged in successfully")
        except:
            print("❌ Login button text did not update")
    
    def test_07_form_loading_states(self):
        """Test form loading states during submission"""
        print("\n🧪 Test 7: Form Loading States")
        self.driver.get(self.base_url)
        
        # Open signup modal
        signup_btn = self._wait_for_element_clickable(By.ID, "signupBtn")
        signup_btn.click()
        
        # Fill form with valid data
        name_field = self.driver.find_element(By.ID, "signupName")
        name_field.clear()
        name_field.send_keys("Loading Test User")
        
        email_field = self.driver.find_element(By.ID, "signupEmail")
        email_field.clear()
        email_field.send_keys(f"loading_test_{self._generate_random_string(8)}@example.com")
        
        password_field = self.driver.find_element(By.ID, "signupPassword")
        password_field.clear()
        password_field.send_keys("password123")
        
        confirm_field = self.driver.find_element(By.ID, "signupConfirmPassword")
        confirm_field.clear()
        confirm_field.send_keys("password123")
        
        # Submit form and check loading state
        submit_btn = self.driver.find_element(By.XPATH, "//form[@id='signupForm']//button[@type='submit']")
        submit_btn.click()
        
        # Check that button shows loading state
        try:
            # Wait for loading text to appear
            self.wait.until(lambda driver: "处理中" in submit_btn.text)
            print("✅ Loading state appeared")
            
            # Wait for loading to complete
            self.wait.until(lambda driver: "注册" in submit_btn.text or "登录" in submit_btn.text)
            print("✅ Loading state completed")
        except TimeoutException:
            print("❌ Loading state test failed")
    
    def test_08_real_time_validation(self):
        """Test real-time validation feedback"""
        print("\n🧪 Test 8: Real-time Validation")
        self.driver.get(self.base_url)
        
        # Open signup modal
        signup_btn = self._wait_for_element_clickable(By.ID, "signupBtn")
        signup_btn.click()
        
        # Test email field real-time validation
        email_field = self.driver.find_element(By.ID, "signupEmail")
        email_field.clear()
        email_field.send_keys("invalid")
        email_field.send_keys("\t")
        
        try:
            error_div = self.driver.find_element(By.ID, "signupEmailError")
            self.assertIn("请输入有效的邮箱地址", error_div.text)
            print("✅ Real-time email validation works")
        except NoSuchElementException:
            print("❌ Real-time email validation failed")
        
        # Test valid email
        email_field.clear()
        email_field.send_keys("valid@example.com")
        email_field.send_keys("\t")
        
        try:
            # Check for green border (success state)
            email_field = self.driver.find_element(By.ID, "signupEmail")
            classes = email_field.get_attribute("class")
            self.assertIn("border-green-500", classes)
            print("✅ Real-time email success state works")
        except:
            print("❌ Real-time email success state failed")
    
    def test_09_modal_switching(self):
        """Test switching between login and signup modals"""
        print("\n🧪 Test 9: Modal Switching")
        self.driver.get(self.base_url)
        
        # Open signup modal
        signup_btn = self._wait_for_element_clickable(By.ID, "signupBtn")
        signup_btn.click()
        
        # Switch to login modal
        switch_to_login = self.driver.find_element(By.ID, "switchToLogin")
        switch_to_login.click()
        
        # Check login modal is visible
        login_modal = self._wait_for_element(By.ID, "loginModal")
        self.assertTrue(login_modal.is_displayed())
        print("✅ Switched to login modal")
        
        # Switch back to signup modal
        switch_to_signup = self.driver.find_element(By.ID, "switchToSignup")
        switch_to_signup.click()
        
        # Check signup modal is visible
        signup_modal = self._wait_for_element(By.ID, "signupModal")
        self.assertTrue(signup_modal.is_displayed())
        print("✅ Switched back to signup modal")
    
    def test_10_error_handling(self):
        """Test various error scenarios"""
        print("\n🧪 Test 10: Error Handling")
        self.driver.get(self.base_url)
        
        # Open signup modal
        signup_btn = self._wait_for_element_clickable(By.ID, "signupBtn")
        signup_btn.click()
        
        # Test empty form submission
        submit_btn = self.driver.find_element(By.XPATH, "//form[@id='signupForm']//button[@type='submit']")
        submit_btn.click()
        
        # Check for validation errors
        try:
            name_error = self.driver.find_element(By.ID, "signupNameError")
            email_error = self.driver.find_element(By.ID, "signupEmailError")
            password_error = self.driver.find_element(By.ID, "signupPasswordError")
            
            self.assertIn("请输入姓名", name_error.text)
            self.assertIn("请输入邮箱地址", email_error.text)
            self.assertIn("请输入密码", password_error.text)
            print("✅ Empty form validation works")
        except NoSuchElementException:
            print("❌ Empty form validation failed")

def run_tests():
    """Run all tests with detailed output"""
    print("🚀 Starting Registration Automation Tests")
    print("=" * 60)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(RegistrationAutomationTest)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\n💥 ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED!")
    else:
        print("\n❌ SOME TESTS FAILED!")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    # Check if server is running
    import requests
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
            success = run_tests()
            exit(0 if success else 1)
        else:
            print("❌ Server is not responding correctly")
            exit(1)
    except requests.exceptions.RequestException:
        print("❌ Server is not running. Please start the server first:")
        print("   python run_local.py")
        exit(1) 