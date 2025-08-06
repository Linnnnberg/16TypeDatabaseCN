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

## Resources

- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Black Documentation](https://black.readthedocs.io/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/) 