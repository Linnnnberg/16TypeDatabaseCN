from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.comment_service import CommentService
from app.services.auth_service import AuthService
from app.schemas.comment import CommentCreate, CommentResponse
from app.database.models import User

router = APIRouter(prefix="/comments", tags=["comments"])
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """Dependency to get current authenticated user"""
    auth_service = AuthService(db)
    return auth_service.get_current_user(credentials.credentials)


@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new comment for a celebrity

    - **celebrity_id**: ID of the celebrity to comment on (required)
    - **content**: Comment content (required, 1-1000 characters)
    - **parent_id**: ID of parent comment for replies (optional)

    Note:
    - Comments can be up to 3 levels deep (replies to replies)
    - Parent comment must belong to the same celebrity
    """
    comment_service = CommentService(db)
    comment = comment_service.create_comment(current_user.id, comment_data)
    return CommentResponse.model_validate(comment)


@router.get("/", response_model=List[CommentResponse])
def get_comments(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    celebrity_id: Optional[str] = Query(None, description="Filter by celebrity ID"),
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    include_replies: bool = Query(
        True, description="Whether to include reply comments"
    ),
    db: Session = Depends(get_db),
):
    """
    Get all comments with optional filters

    - **skip**: Number of records to skip (for pagination)
    - **limit**: Number of records to return (max 1000)
    - **celebrity_id**: Filter comments by celebrity ID
    - **user_id**: Filter comments by user ID
    - **include_replies**: Whether to include reply comments
    """
    comment_service = CommentService(db)

    if celebrity_id:
        comments = comment_service.get_celebrity_comments(
            celebrity_id, skip=skip, limit=limit, include_replies=include_replies
        )
    elif user_id:
        comments = comment_service.get_user_comments(user_id, skip=skip, limit=limit)
    else:
        # Get all comments (you might want to limit this in production)
        comments = comment_service.get_celebrity_comments(
            "", skip=skip, limit=limit, include_replies=include_replies
        )

    return [CommentResponse.model_validate(comment) for comment in comments]


@router.get("/my-comments", response_model=List[CommentResponse])
def get_my_comments(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get current user's comments

    - **skip**: Number of records to skip (for pagination)
    - **limit**: Number of records to return (max 1000)
    """
    comment_service = CommentService(db)
    comments = comment_service.get_user_comments(
        current_user.id, skip=skip, limit=limit
    )
    return [CommentResponse.model_validate(comment) for comment in comments]


@router.get("/user/{user_id}", response_model=List[CommentResponse])
def get_user_comments(
    user_id: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: Session = Depends(get_db),
):
    """
    Get comments by a specific user

    - **user_id**: ID of the user
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Number of records to return (max 1000)
    """
    comment_service = CommentService(db)
    comments = comment_service.get_user_comments(user_id, skip=skip, limit=limit)
    return [CommentResponse.model_validate(comment) for comment in comments]


@router.get("/celebrity/{celebrity_id}", response_model=List[CommentResponse])
def get_celebrity_comments(
    celebrity_id: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    include_replies: bool = Query(
        True, description="Whether to include reply comments"
    ),
    db: Session = Depends(get_db),
):
    """
    Get all comments for a specific celebrity

    - **celebrity_id**: ID of the celebrity
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Number of records to return (max 1000)
    - **include_replies**: Whether to include reply comments
    """
    comment_service = CommentService(db)
    comments = comment_service.get_celebrity_comments(
        celebrity_id, skip=skip, limit=limit, include_replies=include_replies
    )
    return [CommentResponse.model_validate(comment) for comment in comments]


@router.get("/{comment_id}", response_model=CommentResponse)
def get_comment(comment_id: str, db: Session = Depends(get_db)):
    """
    Get a specific comment by ID

    - **comment_id**: Unique identifier of the comment
    """
    comment_service = CommentService(db)
    comment = comment_service.get_comment_by_id(comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )
    return CommentResponse.model_validate(comment)


@router.get("/{comment_id}/replies", response_model=List[CommentResponse])
def get_comment_replies(
    comment_id: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=200, description="Number of records to return"),
    db: Session = Depends(get_db),
):
    """
    Get all replies to a specific comment

    - **comment_id**: ID of the parent comment
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Number of records to return (max 200)
    """
    comment_service = CommentService(db)
    replies = comment_service.get_comment_replies(comment_id, skip=skip, limit=limit)
    return [CommentResponse.model_validate(reply) for reply in replies]


@router.put("/{comment_id}", response_model=CommentResponse)
def update_comment(
    comment_id: str,
    content: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update a comment (only by the user who created it)

    - **comment_id**: Unique identifier of the comment to update
    - **content**: New comment content (1-1000 characters)
    """
    if not content or len(content.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Comment content cannot be empty",
        )

    if len(content) > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Comment content cannot exceed 1000 characters",
        )

    comment_service = CommentService(db)
    comment = comment_service.update_comment(comment_id, current_user.id, content)
    return CommentResponse.model_validate(comment)


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete a comment (only by the user who created it)

    - **comment_id**: Unique identifier of the comment to delete

    Note: Cannot delete comments that have replies
    """
    comment_service = CommentService(db)
    comment_service.delete_comment(comment_id, current_user.id)
    return None


@router.get("/statistics/celebrity/{celebrity_id}")
def get_celebrity_comment_statistics(celebrity_id: str, db: Session = Depends(get_db)):
    """
    Get comment statistics for a celebrity

    - **celebrity_id**: ID of the celebrity

    Returns:
    - Total comments count
    - Top-level comments count
    - Reply comments count
    - Most active commenters
    """
    comment_service = CommentService(db)
    return comment_service.get_comment_statistics(celebrity_id)


@router.get("/statistics/my-stats")
def get_my_comment_statistics(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Get current user's comment statistics

    Returns:
    - Total comments count
    - Top-level comments count
    - Reply comments count
    - Recent comments count (last 7 days)
    """
    comment_service = CommentService(db)
    return comment_service.get_user_comment_statistics(current_user.id)


@router.get("/statistics/user/{user_id}")
def get_user_comment_statistics(user_id: str, db: Session = Depends(get_db)):
    """
    Get comment statistics for a specific user

    - **user_id**: ID of the user

    Returns:
    - Total comments count
    - Top-level comments count
    - Reply comments count
    - Recent comments count (last 7 days)
    """
    comment_service = CommentService(db)
    return comment_service.get_user_comment_statistics(user_id)
