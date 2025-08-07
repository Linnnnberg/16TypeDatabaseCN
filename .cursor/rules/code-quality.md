# Code Quality Standards Rule

## Description
Maintain high code quality standards using established tools and practices to ensure code consistency and reliability.

## Required Tools

### 1. Black Formatting
- Use Black for all Python code formatting
- Line length: 88 characters
- Run before committing: `python -m black app/ tests/`

### 2. Flake8 Linting
- Use Flake8 for linting
- Max line length: 88 characters
- Ignore: E203, W503 (Black compatibility)
- Run: `python -m flake8 app/ tests/ --max-line-length=88 --extend-ignore=E203,W503`

### 3. MyPy Type Checking
- Use MyPy for type checking
- Ignore missing imports: `--ignore-missing-imports`
- Run: `python -m mypy app/ --ignore-missing-imports`

### 4. Security Scanning
- Use Bandit for security scanning
- Use Safety for dependency vulnerability scanning
- Run: `python -m bandit -r app/` and `python -m safety check`

## Code Standards

### 1. Import Order
```python
# Standard library imports
import os
import sys
from pathlib import Path

# Third-party imports
import requests
from fastapi import FastAPI

# Local imports
from app.core.config import settings
from app.database.models import User
```

### 2. Function Documentation
```python
def process_data(data: dict) -> dict:
    """
    Process the input data and return processed result.
    
    Args:
        data: Input data dictionary
        
    Returns:
        Processed data dictionary
        
    Raises:
        ValueError: If data is invalid
    """
    # Implementation
    return processed_data
```

### 3. Error Handling
```python
try:
    result = some_operation()
except SpecificException as e:
    logger.error(f"Specific error occurred: {e}")
    raise
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise RuntimeError(f"Operation failed: {e}")
```

## Examples

### INCORRECT
```python
# Inconsistent formatting
def bad_function( x,y ):
    return x+y

# Missing type hints
def process_data(data):
    return data

# Poor error handling
def risky_operation():
    result = subprocess.run(command)
    return result
```

### CORRECT
```python
# Black-formatted
def good_function(x: int, y: int) -> int:
    return x + y

# Type hints included
def process_data(data: dict) -> dict:
    return data

# Proper error handling
def safe_operation():
    try:
        result = subprocess.run(command, check=True, capture_output=True)
        return result
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {e}")
        raise
```

## Scope
- All Python files
- All test files
- All configuration files
- All documentation files
