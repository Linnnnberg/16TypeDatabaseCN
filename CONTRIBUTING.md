# Contributing to MBTI Roster

Thank you for your interest in contributing to the MBTI Roster project! This document provides guidelines and information for contributors.

## Getting Started

### Prerequisites
- Python 3.8+
- Git
- Basic knowledge of FastAPI, SQLAlchemy, and Pydantic

### Setup Development Environment
1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/16TypeDatabaseCN.git
   cd 16TypeDatabaseCN
   ```
3. **Set up virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements_minimal.txt
   ```
5. **Run setup script**:
   ```bash
   python dev_setup.py --full
   ```

## Development Workflow

### 1. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Follow Coding Standards
- **Read the guidelines**: [DEVELOPMENT_GUIDELINES.md](DEVELOPMENT_GUIDELINES.md)
- **Follow CI/CD rules**: [CI_CD_RULES.md](CI_CD_RULES.md)
- **Use Black formatting**: `python -m black app/ tests/`
- **Run linting**: `python -m flake8 app/ tests/`
- **No emojis in code**: Use text prefixes instead

### 3. Write Tests
- Add unit tests for new functionality
- Ensure all tests pass: `python -m pytest tests/`
- Maintain test coverage above 80%

### 4. Update Documentation
- Update relevant documentation files
- Add docstrings to new functions
- Update API documentation if endpoints change

### 5. Run Local CI
```bash
python run_local_ci.py
python validate_cicd_rules.py
```

### 6. Commit Your Changes
```bash
git add .
git commit -m "feat(scope): descriptive commit message"
```

### 7. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

## Contribution Areas

### High Priority
- **Bug fixes** - Critical issues affecting functionality
- **Security improvements** - Vulnerability fixes
- **Performance optimizations** - Database queries, API responses
- **Test coverage** - Adding missing tests

### Medium Priority
- **New features** - Following the roadmap in [TODO.md](TODO.md)
- **UI/UX improvements** - Frontend enhancements
- **Documentation** - Improving guides and examples
- **Code refactoring** - Cleaner, more maintainable code

### Low Priority
- **Cosmetic changes** - Minor styling updates
- **Documentation typos** - Grammar and spelling fixes
- **Code comments** - Additional inline documentation

## Code Style Guidelines

### Python Code
- Follow PEP 8 style guide
- Use type hints for all functions
- Write descriptive variable and function names
- Keep functions small and focused
- Add docstrings to all public functions

### Example
```python
from typing import List, Optional
from app.schemas.celebrity import CelebrityResponse

async def get_celebrities_by_type(mbti_type: str) -> List[CelebrityResponse]:
    """
    Retrieve celebrities by MBTI type.
    
    Args:
        mbti_type: The MBTI personality type (e.g., 'INTJ')
        
    Returns:
        List of celebrities with the specified MBTI type
        
    Raises:
        ValueError: If mbti_type is invalid
    """
    if not is_valid_mbti_type(mbti_type):
        raise ValueError(f"Invalid MBTI type: {mbti_type}")
    
    # Implementation here
    pass
```

### Commit Messages
Use conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(auth): add JWT token refresh endpoint
fix(ci): resolve test coverage failure
docs(readme): update installation instructions
```

## 🧪 Testing Guidelines

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=app --cov-report=html

# Run specific test file
python -m pytest tests/test_auth.py

# Run with verbose output
python -m pytest tests/ -v
```

### Writing Tests
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)
- Test both success and failure cases
- Mock external dependencies
- Use fixtures for common setup

### Example Test
```python
import pytest
from app.services.auth_service import AuthService

def test_user_registration_success():
    """Test successful user registration"""
    # Arrange
    auth_service = AuthService()
    user_data = {
        "email": "test@example.com",
        "password": "securepassword123",
        "name": "Test User"
    }
    
    # Act
    result = auth_service.register_user(user_data)
    
    # Assert
    assert result.email == user_data["email"]
    assert result.name == user_data["name"]
    assert result.id is not None
```

## 🔍 Review Process

### Pull Request Checklist
Before submitting a PR, ensure:

- [ ] **Code follows guidelines** in [DEVELOPMENT_GUIDELINES.md](DEVELOPMENT_GUIDELINES.md)
- [ ] **All tests pass** locally
- [ ] **No emoji violations** in code
- [ ] **Documentation updated** for new features
- [ ] **Commit messages** follow conventional format
- [ ] **CI/CD validation** passes: `python validate_cicd_rules.py`
- [ ] **Local CI passes**: `python run_local_ci.py`

### Review Guidelines
- Be respectful and constructive
- Focus on code quality and functionality
- Suggest improvements rather than just pointing out issues
- Test the changes locally if possible
- Respond to feedback promptly

## 🐛 Reporting Issues

### Bug Reports
When reporting bugs, include:

1. **Clear description** of the issue
2. **Steps to reproduce** the problem
3. **Expected behavior** vs actual behavior
4. **Environment details** (OS, Python version, etc.)
5. **Error messages** or logs
6. **Screenshots** if applicable

### Feature Requests
For feature requests:

1. **Clear description** of the feature
2. **Use case** and benefits
3. **Proposed implementation** (if you have ideas)
4. **Priority level** (high/medium/low)

## 📞 Getting Help

### Resources
- [Development Guidelines](DEVELOPMENT_GUIDELINES.md) - Coding standards
- [CI/CD Rules](CI_CD_RULES.md) - CI/CD implementation
- [API Documentation](API_DOCUMENTATION.md) - API endpoints
- [Local Development Guide](LOCAL_DEVELOPMENT.md) - Setup instructions

### Communication
- **GitHub Issues** - For bugs and feature requests
- **GitHub Discussions** - For questions and general discussion
- **Pull Request comments** - For code review feedback

## Recognition

Contributors will be recognized in:
- [README.md](README.md) - Contributors section
- [CHANGELOG.md](CHANGELOG.md) - Release notes
- GitHub repository contributors list

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

Thank you for contributing to MBTI Roster!
