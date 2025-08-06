# Development Guidelines

## Code Style and Standards

### Emoji Usage Policy
**NO EMOJIS IN CODE OR PRINT STATEMENTS**

- ❌ **Forbidden**: Using emojis in print statements, log messages, or any code output
- ✅ **Required**: Use descriptive text prefixes instead of emojis

#### Examples:

**❌ WRONG:**
```python
print("✅ Black formatting completed")
print("❌ Formatting failed")
print("🚀 Starting server...")
print("⚠️  Warning message")
```

**✅ CORRECT:**
```python
print("SUCCESS: Black formatting completed")
print("ERROR: Formatting failed")
print("STARTING: Starting server...")
print("WARNING: Warning message")
```

#### Common Replacements:
- `✅` → `SUCCESS:`
- `❌` → `ERROR:`
- `🚀` → `STARTING:`
- `⚠️` → `WARNING:`
- `🔧` → `FIXING:`
- `📝` → `INFO:`

### Why This Rule Exists
1. **CI/CD Compatibility**: Emojis can cause encoding issues in CI/CD pipelines
2. **Terminal Compatibility**: Some terminals don't display emojis correctly
3. **Log Parsing**: Text-based logs are easier to parse and search
4. **Accessibility**: Screen readers handle text better than emoji characters
5. **Cross-Platform**: Ensures consistent output across different operating systems

### Enforcement
- All code must pass Black formatting checks
- All code must pass Flake8 linting checks
- CI/CD pipeline will fail if emojis are found in code
- Use `run_local_ci.py` to check for emoji violations before committing

## CI/CD Implementation Rules

### 1. Test Structure Rules

#### Test File Organization
```
tests/
├── test_basic.py          # Server-independent tests (runs in test job)
├── test_integration.py    # Server-dependent tests (runs in integration job)
├── test_auth.py          # Server-dependent tests
├── test_celebrities.py   # Server-dependent tests
├── test_voting.py        # Server-dependent tests
├── test_comments.py      # Server-dependent tests
├── test_search.py        # Server-dependent tests
└── simple_integration_test.py  # Fallback tests
```

#### Test Job Rules
- **MUST** only run `test_basic.py` in the test job
- **MUST** set up environment variables before running tests
- **MUST** not require a running server
- **MUST** test app imports and basic functionality
- **MUST** generate coverage reports

#### Integration Job Rules
- **MUST** start the server before running tests
- **MUST** run all server-dependent tests
- **MUST** have fallback test options
- **MUST** handle server startup failures gracefully

### 2. Environment Variable Rules

#### Required Environment Variables
```bash
# Always required in CI
CI=true
DATABASE_URL=sqlite:///./test_mbti_roster.db
SECRET_KEY=test-secret-key-for-ci-12345
REDIS_URL=redis://localhost:6379
EMAIL_FROM=noreply@mbti-roster.local
DAILY_VOTE_LIMIT=20
DAILY_NO_REASON_LIMIT=5
NEW_USER_24H_LIMIT=3
DAILY_REGISTRATIONS_PER_IP=3
```

#### Environment Setup Rules
- **MUST** set environment variables before importing app modules
- **MUST** use `echo "VAR=value" >> $GITHUB_ENV` format
- **MUST** set `CI=true` for CI-specific behavior
- **MUST** provide default values for all required settings

### 3. Import and Dependency Rules

#### Import Order Rules
```python
# 1. Standard library imports
import os
import sys
from pathlib import Path

# 2. Third-party imports
import requests
import pytest

# 3. Local app imports (only after environment is set)
from app.core.config import settings
from app.database.models import User
```

#### Dependency Rules
- **MUST** list all dependencies in `requirements_minimal.txt`
- **MUST** specify version constraints for CI tools
- **MUST** install dependencies before running tests
- **MUST** use compatible versions (e.g., `pytest>=7.0.0,<8.0.0`)

### 4. Configuration Rules

#### Pydantic Settings Rules
```python
class Settings(BaseSettings):
    # MUST have default values for CI
    secret_key: str = "test_secret_key"
    
    # MUST handle CI environment
    def __init__(self, **kwargs):
        if "secret_key" not in kwargs and os.getenv("CI"):
            kwargs["secret_key"] = "test-secret-key-for-ci-12345"
        super().__init__(**kwargs)
```

#### Configuration Rules
- **MUST** provide default values for all fields
- **MUST** handle CI environment detection
- **MUST** not require external services in CI
- **MUST** validate configuration on startup

### 5. Server Startup Rules

#### CI Server Rules
- **MUST** use `run_ci_server.py` for CI environments
- **MUST** set environment variables before importing app
- **MUST** include health check endpoints
- **MUST** handle startup failures gracefully
- **MUST** provide clear error messages

#### Health Check Rules
```python
# MUST have health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### 6. Error Handling Rules

#### CI Error Handling
- **MUST** provide clear error messages
- **MUST** include fallback options
- **MUST** not fail silently
- **MUST** log errors appropriately

#### Test Error Handling
```python
# MUST handle import errors gracefully
try:
    from app.core.config import settings
except ImportError as e:
    pytest.fail(f"Failed to import settings: {e}")

# MUST provide fallback for server tests
python -m pytest tests/test_integration.py || python tests/simple_integration_test.py || true
```

## Code Quality Standards

### Python Code Style
- Follow PEP 8 guidelines
- Use Black for automatic formatting (line length: 88 characters)
- Use Flake8 for linting with these settings:
  - Max line length: 88 characters
  - Ignore: E203, W503 (Black compatibility)

### File Naming
- Use snake_case for Python files and directories
- Use descriptive names that indicate purpose
- Avoid abbreviations unless widely understood

### Documentation
- All functions must have docstrings
- Use Google-style docstrings
- Include type hints for all function parameters and return values

### Testing
- Write tests for all new functionality
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)
- Integration tests should be in separate files from unit tests

## Git Workflow

### Commit Messages
- Use conventional commit format: `type(scope): description`
- Examples:
  - `feat(auth): add JWT token validation`
  - `fix(ci): remove emojis from print statements`
  - `docs(readme): update installation instructions`

### Branch Naming
- Use feature branches for new development
- Format: `feature/description` or `fix/description`
- Use descriptive names that indicate the purpose

### Pre-commit Checklist
1. Run `python run_local_ci.py` to check all quality standards
2. Ensure all tests pass
3. Check that no emojis are present in code
4. Verify Black formatting is applied
5. Confirm Flake8 passes without errors

## Environment Setup

### Required Tools
- Python 3.8+
- Black (code formatter)
- Flake8 (linter)
- Pytest (testing)
- MyPy (type checking)

### Local Development
1. Create virtual environment: `python -m venv venv`
2. Activate environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Run local CI: `python run_local_ci.py`

## CI/CD Pipeline

### GitHub Actions
- All code must pass CI checks before merging
- Integration tests run against a live server
- Code quality tools run automatically
- Emoji detection is part of the pipeline

### Environment Variables
- Use `.env` files for local development
- Never commit sensitive information
- Use environment-specific configuration files

## Common Issues and Solutions

### Emoji Detection
If you encounter emoji-related CI failures:
1. Search for emoji characters in your code
2. Replace with appropriate text prefixes
3. Run `python run_local_ci.py` to verify fixes

### Formatting Issues
If Black formatting fails:
1. Run `python -m black app/ tests/` to format code
2. Check for any manual formatting that conflicts with Black
3. Ensure line length doesn't exceed 88 characters

### Import Errors
If you encounter import errors in CI:
1. Check that all dependencies are in `requirements.txt`
2. Verify import paths are correct
3. Ensure no circular imports exist

### Test Failures
If tests fail in CI:
1. Check environment variable setup
2. Verify server startup in integration tests
3. Ensure fallback tests are available
4. Check that basic tests don't require a server

## Best Practices

### Code Organization
- Keep functions small and focused
- Use meaningful variable names
- Avoid deep nesting
- Handle exceptions appropriately

### Performance
- Use async/await for I/O operations
- Optimize database queries
- Cache frequently accessed data
- Monitor memory usage

### Security
- Validate all user inputs
- Use parameterized queries
- Implement proper authentication
- Follow OWASP guidelines

## CI/CD Pipeline Rules

### Job Dependencies
```
test → integration → build → security → deploy-staging
  ↓        ↓         ↓        ↓           ↓
quality  server    docker   security   staging
checks   tests     build    scan       deploy
```

### Required Steps
1. **Code Quality**: Black, Flake8, MyPy, Bandit, Safety
2. **Basic Tests**: Server-independent tests with coverage
3. **Integration Tests**: Server-dependent tests with fallback
4. **Build**: Docker image creation
5. **Security**: Vulnerability scanning
6. **Deploy**: Staging deployment (automatic), Production (manual)

### Failure Handling
- **MUST** provide clear error messages
- **MUST** include fallback options
- **MUST** not fail silently
- **MUST** upload artifacts even on failure

## Implementation Checklist

### Before Committing
- [ ] Run `python run_local_ci.py`
- [ ] Check for emoji usage
- [ ] Verify Black formatting
- [ ] Confirm Flake8 passes
- [ ] Test basic functionality
- [ ] Update documentation if needed

### Before Pushing
- [ ] All local tests pass
- [ ] No emoji violations
- [ ] Code is properly formatted
- [ ] Environment variables are set
- [ ] Fallback options are available

### After CI Failure
- [ ] Check error logs
- [ ] Verify environment setup
- [ ] Test locally with same conditions
- [ ] Fix root cause, not symptoms
- [ ] Update guidelines if needed

## Resources

- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Black Documentation](https://black.readthedocs.io/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions) 