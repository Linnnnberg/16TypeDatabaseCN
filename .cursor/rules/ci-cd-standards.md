# CI/CD Standards Rule

## Description
Follow established CI/CD patterns and standards to ensure smooth pipeline execution and prevent common failures.

## Key Requirements

### 1. Test Structure
- Basic tests (`tests/test_basic.py`) should not require a running server
- Integration tests should be in separate files and clearly marked
- Use `pytest` for all tests, avoid custom test runners

### 2. Environment Variables
- Always provide default values for required settings
- Use `CI=true` environment variable for CI-specific behavior
- Set environment variables before importing app modules

### 3. Configuration Defaults
```python
# app/core/config.py
class Settings(BaseSettings):
    secret_key: str = "test_secret_key"  # MUST have default
    
    def __init__(self, **kwargs):
        if "secret_key" not in kwargs and os.getenv("CI"):
            kwargs["secret_key"] = "test-secret-key-for-ci-12345"
        super().__init__(**kwargs)
```

### 4. GitHub Actions Versions
- Always use the latest stable versions of GitHub Actions
- Check for deprecated actions before using them
- Common deprecated actions:
  - `github/codeql-action/upload-sarif@v1` → `@v3`
  - `github/codeql-action/upload-sarif@v2` → `@v3`

### 5. Error Handling
- Use `check_output=False` for commands that might fail
- Provide fallback mechanisms for critical operations
- Use `|| true` in shell commands when appropriate

## Examples

### INCORRECT
```python
# No default for required setting
class Settings(BaseSettings):
    secret_key: str  # Missing default

# Hardcoded paths
subprocess.run("run_local.py")  # Windows-specific

# No fallback
result = subprocess.run(command, check=True)  # Will crash on failure
```

### CORRECT
```python
# Default values provided
class Settings(BaseSettings):
    secret_key: str = "test_secret_key"

# Cross-platform approach
subprocess.run(["python", "run_ci_server.py"])

# Proper error handling
result = subprocess.run(command, check=False)
if result.returncode != 0:
    # Handle failure gracefully
```

## Scope
- All CI/CD configuration files
- All Python scripts used in CI
- All test files
- All configuration files
