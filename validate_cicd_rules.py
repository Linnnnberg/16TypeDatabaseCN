#!/usr/bin/env python3
"""
CI/CD Rules Validation Script
Validates that code follows all CI/CD implementation rules and guidelines
"""

import os
import sys
import re
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple


class CICDRulesValidator:
    """Validates CI/CD implementation rules"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.success_count = 0
        self.total_checks = 0
        
    def add_error(self, message: str):
        """Add an error message"""
        self.errors.append(message)
        
    def add_warning(self, message: str):
        """Add a warning message"""
        self.warnings.append(message)
        
    def add_success(self, message: str):
        """Add a success message"""
        self.success_count += 1
        print(f"SUCCESS: {message}")
        
    def check_emoji_usage(self) -> bool:
        """Check for emoji usage in code files"""
        print("\n" + "="*60)
        print("CHECKING EMOJI USAGE")
        print("="*60)
        
        emoji_patterns = [
            "✅", "❌", "🚀", "⚠️", "🔧", "📝", "🎉", "🔥", "💯", "✨", "🍰",
            "💥", "💔", "🎯", "⚡", "🌟", "💡", "🔍", "📊", "🎨", "⚙️"
        ]
        
        python_files = list(Path("app").rglob("*.py")) + list(Path("tests").rglob("*.py"))
        emoji_violations = []
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for i, line in enumerate(content.split('\n'), 1):
                        for emoji in emoji_patterns:
                            if emoji in line:
                                emoji_violations.append(f"{file_path}:{i}: {emoji}")
            except Exception as e:
                self.add_warning(f"Could not read {file_path}: {e}")
        
        if emoji_violations:
            print("ERROR: Found emoji usage in code files:")
            for violation in emoji_violations:
                print(f"  - {violation}")
            self.add_error(f"Found {len(emoji_violations)} emoji violations")
            return False
        else:
            self.add_success("No emoji usage found in code files")
            return True
    
    def check_test_structure(self) -> bool:
        """Check test file structure and organization"""
        print("\n" + "="*60)
        print("CHECKING TEST STRUCTURE")
        print("="*60)
        
        required_files = [
            "tests/test_basic.py",
            "tests/test_integration.py",
            "tests/simple_integration_test.py"
        ]
        
        missing_files = []
        for file_path in required_files:
            if not Path(file_path).exists():
                missing_files.append(file_path)
        
        if missing_files:
            print("ERROR: Missing required test files:")
            for file_path in missing_files:
                print(f"  - {file_path}")
            self.add_error(f"Missing {len(missing_files)} required test files")
            return False
        else:
            self.add_success("All required test files exist")
            return True
    
    def check_environment_variables(self) -> bool:
        """Check environment variable setup in CI files"""
        print("\n" + "="*60)
        print("CHECKING ENVIRONMENT VARIABLES")
        print("="*60)
        
        required_vars = [
            "CI=true",
            "DATABASE_URL=",
            "SECRET_KEY=",
            "REDIS_URL=",
            "EMAIL_FROM=",
            "DAILY_VOTE_LIMIT=",
            "DAILY_NO_REASON_LIMIT=",
            "NEW_USER_24H_LIMIT=",
            "DAILY_REGISTRATIONS_PER_IP="
        ]
        
        ci_file = Path(".github/workflows/ci.yml")
        if not ci_file.exists():
            self.add_error("CI workflow file not found")
            return False
        
        try:
            with open(ci_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            missing_vars = []
            for var in required_vars:
                if var not in content:
                    missing_vars.append(var)
            
            if missing_vars:
                print("ERROR: Missing required environment variables in CI:")
                for var in missing_vars:
                    print(f"  - {var}")
                self.add_error(f"Missing {len(missing_vars)} environment variables")
                return False
            else:
                self.add_success("All required environment variables are set")
                return True
                
        except Exception as e:
            self.add_error(f"Could not read CI file: {e}")
            return False
    
    def check_config_defaults(self) -> bool:
        """Check that configuration has proper defaults"""
        print("\n" + "="*60)
        print("CHECKING CONFIGURATION DEFAULTS")
        print("="*60)
        
        config_file = Path("app/core/config.py")
        if not config_file.exists():
            self.add_error("Configuration file not found")
            return False
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for default values
            if 'secret_key: str = "test_secret_key"' not in content:
                self.add_error("Missing default value for secret_key")
                return False
            
            # Check for CI environment handling
            if 'os.getenv("CI")' not in content:
                self.add_error("Missing CI environment detection")
                return False
            
            self.add_success("Configuration has proper defaults and CI handling")
            return True
            
        except Exception as e:
            self.add_error(f"Could not read config file: {e}")
            return False
    
    def check_health_endpoint(self) -> bool:
        """Check that health endpoint exists"""
        print("\n" + "="*60)
        print("CHECKING HEALTH ENDPOINT")
        print("="*60)
        
        main_file = Path("app/main.py")
        if not main_file.exists():
            self.add_error("Main application file not found")
            return False
        
        try:
            with open(main_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if '@app.get("/health")' not in content:
                self.add_error("Health endpoint not found")
                return False
            
            self.add_success("Health endpoint exists")
            return True
            
        except Exception as e:
            self.add_error(f"Could not read main file: {e}")
            return False
    
    def check_ci_server_script(self) -> bool:
        """Check that CI server script exists and is properly configured"""
        print("\n" + "="*60)
        print("CHECKING CI SERVER SCRIPT")
        print("="*60)
        
        ci_server_file = Path("run_ci_server.py")
        if not ci_server_file.exists():
            self.add_error("CI server script not found")
            return False
        
        try:
            with open(ci_server_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            required_elements = [
                "setup_ci_environment",
                "wait_for_server",
                "os.environ[",
                "requests.get",
                "uvicorn"
            ]
            
            missing_elements = []
            for element in required_elements:
                if element not in content:
                    missing_elements.append(element)
            
            if missing_elements:
                print("ERROR: CI server script missing required elements:")
                for element in missing_elements:
                    print(f"  - {element}")
                self.add_error(f"Missing {len(missing_elements)} required elements")
                return False
            else:
                self.add_success("CI server script is properly configured")
                return True
                
        except Exception as e:
            self.add_error(f"Could not read CI server script: {e}")
            return False
    
    def check_fallback_tests(self) -> bool:
        """Check that fallback tests exist"""
        print("\n" + "="*60)
        print("CHECKING FALLBACK TESTS")
        print("="*60)
        
        fallback_file = Path("tests/simple_integration_test.py")
        if not fallback_file.exists():
            self.add_error("Fallback test file not found")
            return False
        
        try:
            with open(fallback_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            required_elements = [
                "requests.get",
                "test_endpoint",
                "main()",
                "sys.exit"
            ]
            
            missing_elements = []
            for element in required_elements:
                if element not in content:
                    missing_elements.append(element)
            
            if missing_elements:
                print("ERROR: Fallback test file missing required elements:")
                for element in missing_elements:
                    print(f"  - {element}")
                self.add_error(f"Missing {len(missing_elements)} required elements")
                return False
            else:
                self.add_success("Fallback tests are properly configured")
                return True
                
        except Exception as e:
            self.add_error(f"Could not read fallback test file: {e}")
            return False
    
    def check_dependencies(self) -> bool:
        """Check that all required dependencies are listed"""
        print("\n" + "="*60)
        print("CHECKING DEPENDENCIES")
        print("="*60)
        
        requirements_file = Path("requirements_minimal.txt")
        if not requirements_file.exists():
            self.add_error("Requirements file not found")
            return False
        
        try:
            with open(requirements_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            required_packages = [
                "fastapi",
                "uvicorn",
                "pytest",
                "requests",
                "sqlalchemy"
            ]
            
            missing_packages = []
            for package in required_packages:
                if package not in content:
                    missing_packages.append(package)
            
            if missing_packages:
                print("ERROR: Missing required packages in requirements:")
                for package in missing_packages:
                    print(f"  - {package}")
                self.add_error(f"Missing {len(missing_packages)} required packages")
                return False
            else:
                self.add_success("All required packages are listed")
                return True
                
        except Exception as e:
            self.add_error(f"Could not read requirements file: {e}")
            return False
    
    def check_import_order(self) -> bool:
        """Check import order in Python files"""
        print("\n" + "="*60)
        print("CHECKING IMPORT ORDER")
        print("="*60)
        
        python_files = list(Path("app").rglob("*.py"))
        import_violations = []
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # Find import lines
                import_lines = []
                for i, line in enumerate(lines, 1):
                    if line.strip().startswith(('import ', 'from ')):
                        import_lines.append((i, line.strip()))
                
                # Check for app imports before environment setup
                for line_num, line in import_lines:
                    if 'from app.' in line and line_num < 10:  # Early in file
                        # Check if environment setup comes before this
                        has_env_setup = False
                        for j in range(line_num):
                            if 'os.environ' in lines[j] or 'CI=true' in lines[j]:
                                has_env_setup = True
                                break
                        
                        if not has_env_setup:
                            import_violations.append(f"{file_path}:{line_num}: {line}")
                            
            except Exception as e:
                self.add_warning(f"Could not check {file_path}: {e}")
        
        if import_violations:
            print("ERROR: Found import order violations:")
            for violation in import_violations:
                print(f"  - {violation}")
            self.add_error(f"Found {len(import_violations)} import order violations")
            return False
        else:
            self.add_success("Import order is correct")
            return True
    
    def run_all_checks(self) -> bool:
        """Run all CI/CD rules validation checks"""
        print("STARTING: CI/CD Rules Validation")
        print("="*60)
        
        checks = [
            ("Emoji Usage", self.check_emoji_usage),
            ("Test Structure", self.check_test_structure),
            ("Environment Variables", self.check_environment_variables),
            ("Configuration Defaults", self.check_config_defaults),
            ("Health Endpoint", self.check_health_endpoint),
            ("CI Server Script", self.check_ci_server_script),
            ("Fallback Tests", self.check_fallback_tests),
            ("Dependencies", self.check_dependencies),
            ("Import Order", self.check_import_order),
        ]
        
        passed_checks = 0
        total_checks = len(checks)
        
        for check_name, check_func in checks:
            self.total_checks += 1
            print(f"\nRunning: {check_name}")
            try:
                if check_func():
                    passed_checks += 1
            except Exception as e:
                self.add_error(f"{check_name} check failed with exception: {e}")
        
        # Print summary
        print("\n" + "="*60)
        print("CI/CD RULES VALIDATION SUMMARY")
        print("="*60)
        
        print(f"Total checks: {total_checks}")
        print(f"Passed checks: {passed_checks}")
        print(f"Failed checks: {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}")
        
        if self.errors:
            print(f"\nERROR: ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")
        
        if self.warnings:
            print(f"\nWARNING: WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        if not self.errors:
            print(f"\nSUCCESS: ALL CI/CD RULES VALIDATION CHECKS PASSED!")
            print("Your code follows all CI/CD implementation guidelines.")
        else:
            print(f"\nERROR: {len(self.errors)} CI/CD RULES VIOLATIONS FOUND.")
            print("Please fix the issues before committing.")
        
        return len(self.errors) == 0


def main():
    """Main function"""
    validator = CICDRulesValidator()
    
    try:
        success = validator.run_all_checks()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nERROR: Validation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nERROR: Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
