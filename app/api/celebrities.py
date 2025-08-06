from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.celebrity_service import CelebrityService
from app.services.auth_service import AuthService
from app.schemas.celebrity import CelebrityCreate, CelebrityUpdate, CelebrityResponse
from app.database.models import User, UserRole

router = APIRouter(prefix="/celebrities", tags=["celebrities"])
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """Dependency to get current authenticated user"""
    auth_service = AuthService(db)
    return auth_service.get_current_user(credentials.credentials)


def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Dependency to get current admin user"""
    if current_user.role != UserRole.SYSTEM:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only system users can perform this action",
        )
    return current_user


@router.post("/", response_model=CelebrityResponse, status_code=status.HTTP_201_CREATED)
def create_celebrity(
    celebrity_data: CelebrityCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """
    Create a new celebrity (Admin only)

    - **name**: Celebrity's name (required)
    - **name_en**: Celebrity's English name (optional)
    - **description**: Celebrity's description (optional)
    - **image_url**: Celebrity's image URL (optional)
    """
    celebrity_service = CelebrityService(db)
    celebrity = celebrity_service.create_celebrity(celebrity_data)
    return CelebrityResponse.model_validate(celebrity)


@router.get("/", response_model=List[CelebrityResponse])
def get_celebrities(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    search: Optional[str] = Query(
        None, description="Search term for name or description"
    ),
    db: Session = Depends(get_db),
):
    """
    Get all celebrities with optional search and pagination

    - **skip**: Number of records to skip (for pagination)
    - **limit**: Number of records to return (max 1000)
    - **search**: Search term to filter by name or description
    """
    celebrity_service = CelebrityService(db)
    celebrities = celebrity_service.get_all_celebrities(
        skip=skip, limit=limit, search=search
    )
    return [CelebrityResponse.model_validate(celebrity) for celebrity in celebrities]


@router.get("/popular", response_model=List[CelebrityResponse])
def get_popular_celebrities(
    limit: int = Query(
        10, ge=1, le=50, description="Number of popular celebrities to return"
    ),
    db: Session = Depends(get_db),
):
    """
    Get popular celebrities (most voted)

    - **limit**: Number of celebrities to return (max 50)
    """
    celebrity_service = CelebrityService(db)
    celebrities = celebrity_service.get_popular_celebrities(limit=limit)
    return [CelebrityResponse.model_validate(celebrity) for celebrity in celebrities]


@router.get("/tag/{tag_name}", response_model=List[CelebrityResponse])
def get_celebrities_by_tag(
    tag_name: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: Session = Depends(get_db),
):
    """
    Get celebrities by tag

    - **tag_name**: Name of the tag to filter by
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Number of records to return (max 1000)
    """
    celebrity_service = CelebrityService(db)
    celebrities = celebrity_service.get_celebrities_by_tag(
        tag_name, skip=skip, limit=limit
    )
    return [CelebrityResponse.model_validate(celebrity) for celebrity in celebrities]


@router.get("/{celebrity_id}", response_model=CelebrityResponse)
def get_celebrity(celebrity_id: str, db: Session = Depends(get_db)):
    """
    Get celebrity by ID

    - **celebrity_id**: Unique identifier of the celebrity
    """
    celebrity_service = CelebrityService(db)
    celebrity = celebrity_service.get_celebrity_by_id(celebrity_id)
    if not celebrity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Celebrity not found"
        )
    return CelebrityResponse.model_validate(celebrity)


@router.get("/search/{name}", response_model=CelebrityResponse)
def get_celebrity_by_name(name: str, db: Session = Depends(get_db)):
    """
    Get celebrity by name (Chinese or English)

    - **name**: Celebrity's name (Chinese or English)
    """
    celebrity_service = CelebrityService(db)
    celebrity = celebrity_service.get_celebrity_by_name(name)
    if not celebrity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Celebrity not found"
        )
    return CelebrityResponse.model_validate(celebrity)


@router.put("/{celebrity_id}", response_model=CelebrityResponse)
def update_celebrity(
    celebrity_id: str,
    celebrity_data: CelebrityUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """
    Update celebrity information (Admin only)

    - **celebrity_id**: Unique identifier of the celebrity
    - **name**: New name (optional)
    - **name_en**: New English name (optional)
    - **description**: New description (optional)
    - **image_url**: New image URL (optional)
    """
    celebrity_service = CelebrityService(db)
    celebrity = celebrity_service.update_celebrity(celebrity_id, celebrity_data)
    return CelebrityResponse.model_validate(celebrity)


@router.delete("/{celebrity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_celebrity(
    celebrity_id: str,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """
    Delete a celebrity (Admin only)

    - **celebrity_id**: Unique identifier of the celebrity

    Note: Cannot delete celebrities with existing votes or comments
    """
    celebrity_service = CelebrityService(db)
    celebrity_service.delete_celebrity(celebrity_id)
    return None


@router.post("/{celebrity_id}/tags/{tag_name}", status_code=status.HTTP_201_CREATED)
def add_tag_to_celebrity(
    celebrity_id: str,
    tag_name: str,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """
    Add a tag to a celebrity (Admin only)

    - **celebrity_id**: Unique identifier of the celebrity
    - **tag_name**: Name of the tag to add
    """
    celebrity_service = CelebrityService(db)
    celebrity_service.add_tag_to_celebrity(celebrity_id, tag_name)
    return {"message": f"Tag '{tag_name}' added to celebrity successfully"}


@router.delete(
    "/{celebrity_id}/tags/{tag_name}", status_code=status.HTTP_204_NO_CONTENT
)
def remove_tag_from_celebrity(
    celebrity_id: str,
    tag_name: str,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """
    Remove a tag from a celebrity (Admin only)

    - **celebrity_id**: Unique identifier of the celebrity
    - **tag_name**: Name of the tag to remove
    """
    celebrity_service = CelebrityService(db)
    celebrity_service.remove_tag_from_celebrity(celebrity_id, tag_name)
    return None
