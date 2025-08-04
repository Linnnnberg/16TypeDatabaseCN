from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.schemas.auth import UserCreate, UserLogin, Token, UserResponse
from app.schemas.user import UserProfile, UserUpdate
from app.database.models import User

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Dependency to get current authenticated user"""
    auth_service = AuthService(db)
    return auth_service.get_current_user(credentials.credentials)

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user account
    
    - **email**: User's email address (must be unique)
    - **password**: User's password (minimum 6 characters)
    - **name**: User's display name
    """
    auth_service = AuthService(db)
    user = auth_service.register_user(user_data)
    return UserResponse.model_validate(user)

@router.post("/login", response_model=Token)
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Login user and get access token
    
    - **email**: User's email address
    - **password**: User's password
    """
    auth_service = AuthService(db)
    return auth_service.login_user(user_data)

@router.get("/me", response_model=UserProfile)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """
    Get current user's profile information
    
    Requires authentication token
    """
    return UserProfile.model_validate(current_user)

@router.put("/me", response_model=UserProfile)
def update_current_user_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update current user's profile information
    
    - **name**: New display name (optional)
    - **is_active**: Account status (optional, admin only)
    
    Requires authentication token
    """
    user_service = UserService(db)
    return user_service.update_user(current_user.id, user_data)

@router.delete("/me", response_model=UserProfile)
def deactivate_current_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Deactivate current user's account
    
    Requires authentication token
    """
    user_service = UserService(db)
    return user_service.deactivate_user(current_user.id)

# Admin endpoints (for system users)
@router.post("/admin/create-system-user", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_system_user(
    user_data: UserCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a system user (admin only)
    
    - **email**: User's email address
    - **password**: User's password
    - **name**: User's display name
    
    Requires SYSTEM role authentication
    """
    if current_user.role.value != "SYSTEM":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only system users can create system accounts"
        )
    
    auth_service = AuthService(db)
    user = auth_service.create_system_user(
        user_data.email,
        user_data.password,
        user_data.name
    )
    return UserResponse.model_validate(user) 