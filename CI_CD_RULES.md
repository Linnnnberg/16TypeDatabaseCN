# CI/CD Rules - Quick Reference

## 🚨 Critical Rules (Must Follow)

### 1. No Emojis in Code
```python
# ❌ WRONG
print("✅ Success!")
print("❌ Error occurred")

# ✅ CORRECT
print("SUCCESS: Operation completed")
print("ERROR: Operation failed")
```

### 2. Environment Variables Setup
```yaml
# .github/workflows/ci.yml
- name: Set up test environment
  run: |
    echo "CI=true" >> $GITHUB_ENV
    echo "DATABASE_URL=sqlite:///./test_mbti_roster.db" >> $GITHUB_ENV
    echo "SECRET_KEY=test-secret-key-for-ci-12345" >> $GITHUB_ENV
    # ... other variables
```

### 3. Test Structure
```
tests/
├── test_basic.py          # Server-independent (test job)
├── test_integration.py    # Server-dependent (integration job)
├── test_auth.py          # Server-dependent
├── test_celebrities.py   # Server-dependent
└── simple_integration_test.py  # Fallback
```

### 4. Configuration Defaults
```python
# app/core/config.py
class Settings(BaseSettings):
    secret_key: str = "test_secret_key"  # MUST have default
    
    def __init__(self, **kwargs):
        if "secret_key" not in kwargs and os.getenv("CI"):
            kwargs["secret_key"] = "test-secret-key-for-ci-12345"
        super().__init__(**kwargs)
```

## 🔧 Implementation Rules

### Test Job Rules
- **MUST** only run `test_basic.py`
- **MUST** set environment variables before tests
- **MUST** not require a running server
- **MUST** generate coverage reports

### Integration Job Rules
- **MUST** start server before tests
- **MUST** run server-dependent tests
- **MUST** have fallback options
- **MUST** handle startup failures

### Import Order Rules
```python
# 1. Standard library
import os
import sys

# 2. Third-party
import requests
import pytest

# 3. Local app (after environment setup)
from app.core.config import settings
```

## 📋 Pre-Commit Checklist

### Before Committing
- [ ] Run `python run_local_ci.py`
- [ ] Run `python validate_cicd_rules.py`
- [ ] Check for emoji usage
- [ ] Verify Black formatting
- [ ] Confirm Flake8 passes
- [ ] Test basic functionality

### Before Pushing
- [ ] All local tests pass
- [ ] No emoji violations
- [ ] Code is properly formatted
- [ ] Environment variables are set
- [ ] Fallback options are available

## 🛠️ Tools and Commands

### Local Development
```bash
# Run full CI/CD pipeline locally
python run_local_ci.py

# Validate CI/CD rules
python validate_cicd_rules.py

# Format code
python -m black app/ tests/

# Lint code
python -m flake8 app/ tests/

# Run tests
python -m pytest tests/test_basic.py -v
```

### Pre-commit Hooks
```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run pre-commit hooks manually
pre-commit run --all-files
```

## 🚨 Common Issues and Solutions

### Issue: "secret_key missing"
**Solution**: Add default value in `app/core/config.py`
```python
secret_key: str = "test_secret_key"
```

### Issue: "ImportError in CI"
**Solution**: Set environment variables before imports
```python
# Set environment first
os.environ["CI"] = "true"
os.environ["SECRET_KEY"] = "test-key"

# Then import app modules
from app.core.config import settings
```

### Issue: "Tests fail in CI"
**Solution**: Check test structure
- Basic tests in `test_basic.py` (no server required)
- Integration tests in other files (server required)

### Issue: "Emoji in code"
**Solution**: Replace with text prefixes
```python
# Replace ✅ with SUCCESS:
# Replace ❌ with ERROR:
# Replace 🚀 with STARTING:
# Replace ⚠️ with WARNING:
```

## 📁 Required Files

### CI/CD Files
- `.github/workflows/ci.yml` - GitHub Actions workflow
- `run_ci_server.py` - CI server startup script
- `test_config.py` - Configuration testing script
- `validate_cicd_rules.py` - Rules validation script

### Test Files
- `tests/test_basic.py` - Server-independent tests
- `tests/simple_integration_test.py` - Fallback tests
- `tests/test_integration.py` - Server-dependent tests

### Configuration Files
- `app/core/config.py` - Application configuration
- `requirements_minimal.txt` - Dependencies
- `.pre-commit-config.yaml` - Pre-commit hooks

## 🔍 Validation Commands

### Quick Validation
```bash
# Check all rules
python validate_cicd_rules.py

# Check emoji usage only
python -c "
import sys
from pathlib import Path
emoji_patterns = ['✅', '❌', '🚀', '⚠️']
violations = []
for file_path in Path('.').rglob('*.py'):
    with open(file_path, 'r') as f:
        for i, line in enumerate(f, 1):
            for emoji in emoji_patterns:
                if emoji in line:
                    violations.append(f'{file_path}:{i}')
if violations:
    print('Found emoji violations:', violations)
    sys.exit(1)
print('No emoji violations found')
"
```

### Environment Check
```bash
# Check environment variables
python -c "
import os
required = ['CI', 'DATABASE_URL', 'SECRET_KEY']
missing = [var for var in required if not os.getenv(var)]
if missing:
    print('Missing environment variables:', missing)
    exit(1)
print('All required environment variables set')
"
```

## 📊 CI/CD Pipeline Flow

```
Code Push
    ↓
Pre-commit Hooks
    ↓
GitHub Actions
    ↓
Test Job (Basic Tests)
    ↓
Integration Job (Server Tests)
    ↓
Build Job (Docker)
    ↓
Security Scan
    ↓
Deploy to Staging
    ↓
Manual Production Deploy
```

## 🎯 Success Criteria

### CI/CD Pipeline Success
- ✅ All pre-commit hooks pass
- ✅ Test job passes with coverage
- ✅ Integration job passes with server
- ✅ Build job creates Docker image
- ✅ Security scan passes
- ✅ Deployment succeeds

### Code Quality Success
- ✅ No emoji usage
- ✅ Black formatting applied
- ✅ Flake8 linting passes
- ✅ MyPy type checking passes
- ✅ All tests pass
- ✅ Documentation updated

## 📞 Emergency Procedures

### If CI/CD Pipeline Fails
1. Check error logs in GitHub Actions
2. Run `python validate_cicd_rules.py` locally
3. Fix the root cause, not symptoms
4. Test locally with same conditions
5. Update guidelines if needed

### If Tests Fail
1. Check environment variable setup
2. Verify server startup in integration tests
3. Ensure fallback tests are available
4. Check that basic tests don't require server

### If Build Fails
1. Check Dockerfile syntax
2. Verify all dependencies are listed
3. Check for missing files
4. Test Docker build locally

## 📚 Additional Resources

- [Development Guidelines](DEVELOPMENT_GUIDELINES.md) - Comprehensive guidelines
- [CI/CD Guide](CI_CD_GUIDE.md) - Detailed CI/CD documentation
- [API Documentation](docs/) - Generated API docs
- [GitHub Actions Logs](https://github.com/Linnnnberg/16TypeDatabaseCN/actions) - CI/CD logs

---

**Remember**: These rules are designed to prevent the issues we've encountered and ensure smooth CI/CD processes. Follow them strictly to maintain code quality and pipeline reliability.
