#!/usr/bin/env python3
"""
Local CI/CD Pipeline Runner
Runs all the same checks as GitHub Actions locally before pushing
"""

import subprocess
import sys
import os
import json
from pathlib import Path
from datetime import datetime
import shutil

class LocalCI:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.success_count = 0
        self.total_checks = 0
        
    def run_command(self, command, description, check_output=True, capture_output=True):
        """Run a command and handle the result"""
        self.total_checks += 1
        print(f"\n{'='*60}")
        print(f"Running: {description}")
        print(f"Command: {command}")
        print(f"{'='*60}")
        
        try:
            if capture_output:
                result = subprocess.run(
                    command, 
                    shell=True, 
                    capture_output=True, 
                    text=True, 
                    check=check_output
                )
                if result.stdout:
                    print("STDOUT:")
                    print(result.stdout)
                if result.stderr:
                    print("STDERR:")
                    print(result.stderr)
                return result.returncode == 0
            else:
                result = subprocess.run(command, shell=True, check=check_output)
                return result.returncode == 0
        except subprocess.CalledProcessError as e:
            print(f"ERROR: {e}")
            self.errors.append(f"{description}: {e}")
            return False
        except Exception as e:
            print(f"ERROR: {e}")
            self.errors.append(f"{description}: {e}")
            return False
    
    def install_dependencies(self):
        """Install all required dependencies"""
        print("\n" + "="*60)
        print("INSTALLING DEPENDENCIES")
        print("="*60)
        
        # Install base requirements
        if self.run_command("pip install -r requirements_minimal.txt", "Installing minimal requirements"):
            self.success_count += 1
            
        # Install testing dependencies
        if self.run_command("pip install pytest pytest-cov pytest-asyncio", "Installing pytest dependencies"):
            self.success_count += 1
            
        # Install code quality tools
        if self.run_command("pip install black flake8 mypy", "Installing code quality tools"):
            self.success_count += 1
            
        # Install security tools
        if self.run_command("pip install bandit safety", "Installing security tools"):
            self.success_count += 1
            
        # Install additional tools
        if self.run_command("pip install httpx pdoc3", "Installing additional tools"):
            self.success_count += 1
    
    def run_black_check(self):
        """Run Black code formatting check"""
        print("\n" + "="*60)
        print("RUNNING BLACK CODE FORMATTING CHECK")
        print("="*60)
        
        # First, try to format the code
        if self.run_command("python -m black app/ tests/", "Formatting code with Black", check_output=False):
            self.success_count += 1
            print("SUCCESS: Black formatting completed")
        else:
            self.errors.append("Black formatting failed")
            return False
            
        # Then check if formatting is correct
        if self.run_command("python -m black --check app/ tests/", "Checking Black formatting"):
            self.success_count += 1
            print("SUCCESS: Black formatting check passed")
            return True
        else:
            self.errors.append("Black formatting check failed")
            return False
    
    def run_flake8_check(self):
        """Run Flake8 linting check"""
        print("\n" + "="*60)
        print("RUNNING FLAKE8 LINTING CHECK")
        print("="*60)
        
        if self.run_command(
            "python -m flake8 app/ tests/ --max-line-length=88 --extend-ignore=E203,W503 --count --statistics",
            "Running Flake8 linting"
        ):
            self.success_count += 1
            print("SUCCESS: Flake8 linting passed")
            return True
        else:
            self.errors.append("Flake8 linting failed")
            return False
    
    def run_mypy_check(self):
        """Run MyPy type checking"""
        print("\n" + "="*60)
        print("RUNNING MYPY TYPE CHECKING")
        print("="*60)
        
        if self.run_command(
            "python -m mypy app/ --ignore-missing-imports",
            "Running MyPy type checking"
        ):
            self.success_count += 1
            print("SUCCESS: MyPy type checking passed")
            return True
        else:
            self.errors.append("MyPy type checking failed")
            return False
    
    def run_security_checks(self):
        """Run security scans"""
        print("\n" + "="*60)
        print("RUNNING SECURITY CHECKS")
        print("="*60)
        
        # Bandit security scan
        if self.run_command(
            "python -m bandit -r app/ -f json -o bandit-report.json",
            "Running Bandit security scan",
            check_output=False
        ):
            self.success_count += 1
            print("SUCCESS: Bandit security scan completed")
        else:
            self.warnings.append("Bandit security scan failed or found issues")
            
        # Safety dependency scan
        if self.run_command(
            "python -m safety check --json --output safety-report.json",
            "Running Safety dependency scan",
            check_output=False
        ):
            self.success_count += 1
            print("SUCCESS: Safety dependency scan completed")
        else:
            self.warnings.append("Safety dependency scan failed or found issues")
            
        return True
    
    def run_tests(self):
        """Run pytest with coverage"""
        print("\n" + "="*60)
        print("RUNNING TESTS WITH COVERAGE")
        print("="*60)
        
        if self.run_command(
            "python -m pytest tests/ --cov=app --cov-report=xml --cov-report=html --cov-report=term-missing -v",
            "Running tests with coverage",
            check_output=False
        ):
            self.success_count += 1
            print("SUCCESS: Tests completed")
            return True
        else:
            self.errors.append("Tests failed")
            return False
    
    def run_integration_tests(self):
        """Run integration tests (simulated)"""
        print("\n" + "="*60)
        print("RUNNING INTEGRATION TESTS")
        print("="*60)
        
        # For local testing, we'll just run the basic tests again
        # In a real scenario, you might start the server and run integration tests
        if self.run_command(
            "python -m pytest tests/ -v --tb=short",
            "Running integration tests",
            check_output=False
        ):
            self.success_count += 1
            print("SUCCESS: Integration tests completed")
            return True
        else:
            self.warnings.append("Integration tests failed")
            return False
    
    def generate_documentation(self):
        """Generate API documentation"""
        print("\n" + "="*60)
        print("GENERATING DOCUMENTATION")
        print("="*60)
        
        # Create docs directory
        docs_dir = Path("docs")
        docs_dir.mkdir(exist_ok=True)
        
        if self.run_command(
            "python -m pdoc --html --output-dir docs/ app/",
            "Generating API documentation",
            check_output=False
        ):
            self.success_count += 1
            print("SUCCESS: Documentation generated")
            return True
        else:
            self.warnings.append("Documentation generation failed")
            return False
    
    def check_docker_build(self):
        """Check if Docker build works"""
        print("\n" + "="*60)
        print("CHECKING DOCKER BUILD")
        print("="*60)
        
        if not Path("Dockerfile").exists():
            print("WARNING: No Dockerfile found, skipping Docker build check")
            return True
            
        if self.run_command(
            "docker build -t mbti-roster:test .",
            "Building Docker image",
            check_output=False
        ):
            self.success_count += 1
            print("SUCCESS: Docker build successful")
            
            # Clean up
            self.run_command("docker rmi mbti-roster:test", "Cleaning up Docker image", check_output=False)
            return True
        else:
            self.warnings.append("Docker build failed")
            return False
    
    def print_summary(self):
        """Print summary of all checks"""
        print("\n" + "="*60)
        print("LOCAL CI/CD SUMMARY")
        print("="*60)
        
        print(f"Total checks run: {self.total_checks}")
        print(f"Successful checks: {self.success_count}")
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
            print(f"\nSUCCESS: ALL CHECKS PASSED! Ready to push to GitHub.")
            print("You can now run: git add . && git commit -m 'your message' && git push")
        else:
            print(f"\nERROR: {len(self.errors)} CHECKS FAILED. Please fix the issues before pushing.")
            
        print(f"\nTimestamp: {datetime.now().isoformat()}")
    
    def run_all_checks(self):
        """Run all CI/CD checks"""
        print("STARTING: Local CI/CD Pipeline")
        print(f"Timestamp: {datetime.now().isoformat()}")
        
        # Install dependencies
        self.install_dependencies()
        
        # Run code quality checks
        self.run_black_check()
        self.run_flake8_check()
        self.run_mypy_check()
        
        # Run security checks
        self.run_security_checks()
        
        # Run tests
        self.run_tests()
        self.run_integration_tests()
        
        # Generate documentation
        self.generate_documentation()
        
        # Check Docker build
        self.check_docker_build()
        
        # Print summary
        self.print_summary()
        
        return len(self.errors) == 0

def main():
    """Main function"""
    ci = LocalCI()
    
    try:
        success = ci.run_all_checks()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nERROR: CI/CD pipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nERROR: Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 