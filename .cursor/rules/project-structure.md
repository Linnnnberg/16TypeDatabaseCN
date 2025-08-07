# Project Structure Rule

## Description
Maintain consistent project structure and organization to ensure code maintainability and team collaboration.

## Directory Structure

```
16TypeDatabaseCN/
├── app/                    # Main application code
│   ├── api/               # API endpoints
│   ├── core/              # Core configuration and utilities
│   ├── database/          # Database models and connection
│   ├── schemas/           # Pydantic schemas
│   └── services/          # Business logic services
├── tests/                 # Test files
│   ├── test_basic.py      # Server-independent tests
│   ├── test_integration.py # Server-dependent tests
│   └── simple_integration_test.py # Fallback tests
├── templates/             # HTML templates
├── static/                # Static files (CSS, JS)
├── docs/                  # Generated documentation
├── data_uploads/          # Data import files
└── .github/workflows/     # CI/CD workflows
```

## File Naming Conventions

### 1. Python Files
- Use snake_case: `user_service.py`, `auth_endpoints.py`
- Test files: `test_*.py` or `*_test.py`
- Configuration files: `config.py`, `settings.py`

### 2. Template Files
- Use snake_case: `base.html`, `user_profile.html`
- Page templates: `index.html`, `about.html`

### 3. Configuration Files
- Use kebab-case: `requirements-minimal.txt`
- Environment files: `.env`, `.env.example`

## Import Organization

### 1. Module Imports
```python
# app/api/celebrities.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.database import get_db
from app.schemas.celebrity import CelebrityCreate, CelebrityResponse
from app.services.celebrity_service import CelebrityService
```

### 2. Relative vs Absolute Imports
- Use absolute imports for app modules: `from app.core.config import settings`
- Use relative imports sparingly and only within the same package

## Code Organization

### 1. Class Structure
```python
class UserService:
    """Service class for user operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user."""
        # Implementation
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        # Implementation
```

### 2. Function Organization
```python
# Constants at the top
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Helper functions
def validate_pagination(page: int, size: int) -> tuple[int, int]:
    """Validate and normalize pagination parameters."""
    # Implementation

# Main functions
def get_celebrities(
    db: Session,
    page: int = 1,
    size: int = DEFAULT_PAGE_SIZE,
    mbti_type: Optional[str] = None
) -> dict:
    """Get paginated list of celebrities."""
    # Implementation
```

## Examples

### INCORRECT
```python
# Wrong file location
# app/main.py - should be in app/api/
@app.get("/users")
def get_users():
    pass

# Inconsistent naming
class userService:  # Should be UserService
    pass

# Poor organization
import os
import sys
from app.core.config import settings  # Mixed import order
import requests
```

### CORRECT
```python
# Proper file location
# app/api/users.py
@router.get("/users")
def get_users():
    pass

# Consistent naming
class UserService:
    pass

# Proper import order
import os
import sys
import requests
from app.core.config import settings
```

## Scope
- All project files and directories
- All import statements
- All class and function definitions
- All configuration files
