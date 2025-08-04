from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.vote_service import VoteService
from app.services.auth_service import AuthService
from app.schemas.vote import VoteCreate, VoteResponse
from app.database.models import User, MBTIType

router = APIRouter(prefix="/votes", tags=["votes"])
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Dependency to get current authenticated user"""
    auth_service = AuthService(db)
    return auth_service.get_current_user(credentials.credentials)

@router.post("/", response_model=VoteResponse, status_code=status.HTTP_201_CREATED)
def create_vote(
    vote_data: VoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new vote for a celebrity
    
    - **celebrity_id**: ID of the celebrity to vote for (required)
    - **mbti_type**: MBTI personality type (required)
    - **reason**: Reason for the vote (optional)
    
    Note: 
    - You can only vote once per celebrity
    - Daily limit: 10 votes per day
    - Reason is optional but encouraged
    """
    vote_service = VoteService(db)
    vote = vote_service.create_vote(current_user.id, vote_data)
    return VoteResponse.model_validate(vote)

@router.get("/", response_model=List[VoteResponse])
def get_votes(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    celebrity_id: Optional[str] = Query(None, description="Filter by celebrity ID"),
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    mbti_type: Optional[MBTIType] = Query(None, description="Filter by MBTI type"),
    db: Session = Depends(get_db)
):
    """
    Get all votes with optional filters
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Number of records to return (max 1000)
    - **celebrity_id**: Filter votes by celebrity ID
    - **user_id**: Filter votes by user ID
    - **mbti_type**: Filter votes by MBTI type
    """
    vote_service = VoteService(db)
    votes = vote_service.get_all_votes(
        skip=skip, 
        limit=limit, 
        celebrity_id=celebrity_id,
        user_id=user_id,
        mbti_type=mbti_type
    )
    return [VoteResponse.model_validate(vote) for vote in votes]

@router.get("/my-votes", response_model=List[VoteResponse])
def get_my_votes(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's votes
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Number of records to return (max 1000)
    """
    vote_service = VoteService(db)
    votes = vote_service.get_user_votes(current_user.id, skip=skip, limit=limit)
    return [VoteResponse.model_validate(vote) for vote in votes]

@router.get("/user/{user_id}", response_model=List[VoteResponse])
def get_user_votes(
    user_id: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Get votes by a specific user
    
    - **user_id**: ID of the user
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Number of records to return (max 1000)
    """
    vote_service = VoteService(db)
    votes = vote_service.get_user_votes(user_id, skip=skip, limit=limit)
    return [VoteResponse.model_validate(vote) for vote in votes]

@router.get("/celebrity/{celebrity_id}", response_model=List[VoteResponse])
def get_celebrity_votes(
    celebrity_id: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Get all votes for a specific celebrity
    
    - **celebrity_id**: ID of the celebrity
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Number of records to return (max 1000)
    """
    vote_service = VoteService(db)
    votes = vote_service.get_celebrity_votes(celebrity_id, skip=skip, limit=limit)
    return [VoteResponse.model_validate(vote) for vote in votes]

@router.get("/{vote_id}", response_model=VoteResponse)
def get_vote(
    vote_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific vote by ID
    
    - **vote_id**: Unique identifier of the vote
    """
    vote_service = VoteService(db)
    vote = vote_service.get_vote_by_id(vote_id)
    if not vote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vote not found"
        )
    return VoteResponse.model_validate(vote)

@router.delete("/{vote_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vote(
    vote_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a vote (only by the user who created it)
    
    - **vote_id**: Unique identifier of the vote to delete
    """
    vote_service = VoteService(db)
    vote_service.delete_vote(vote_id, current_user.id)
    return None

@router.get("/statistics/celebrity/{celebrity_id}")
def get_celebrity_vote_statistics(
    celebrity_id: str,
    db: Session = Depends(get_db)
):
    """
    Get vote statistics for a celebrity
    
    - **celebrity_id**: ID of the celebrity
    
    Returns:
    - Total votes count
    - Votes with/without reasons
    - MBTI type distribution
    - Top voted MBTI type
    """
    vote_service = VoteService(db)
    return vote_service.get_celebrity_vote_statistics(celebrity_id)

@router.get("/statistics/my-stats")
def get_my_vote_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's vote statistics
    
    Returns:
    - Total votes count
    - Today's votes and remaining votes
    - MBTI type distribution
    - Favorite MBTI type
    - Recent daily statistics
    """
    vote_service = VoteService(db)
    return vote_service.get_user_vote_statistics(current_user.id)

@router.get("/statistics/user/{user_id}")
def get_user_vote_statistics(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get vote statistics for a specific user
    
    - **user_id**: ID of the user
    
    Returns:
    - Total votes count
    - Today's votes and remaining votes
    - MBTI type distribution
    - Favorite MBTI type
    - Recent daily statistics
    """
    vote_service = VoteService(db)
    return vote_service.get_user_vote_statistics(user_id)

@router.get("/popular-celebrities")
def get_popular_celebrities_by_votes(
    limit: int = Query(10, ge=1, le=50, description="Number of celebrities to return"),
    db: Session = Depends(get_db)
):
    """
    Get celebrities ordered by number of votes
    
    - **limit**: Number of celebrities to return (max 50)
    
    Returns:
    - Celebrities with vote counts
    - Top MBTI type for each celebrity
    """
    vote_service = VoteService(db)
    return vote_service.get_popular_celebrities_by_votes(limit=limit)

@router.get("/mbti-types")
def get_mbti_types():
    """
    Get all available MBTI personality types
    
    Returns list of all 16 MBTI types
    """
    return [
        {"value": mbti_type.value, "name": mbti_type.value}
        for mbti_type in MBTIType
    ] 