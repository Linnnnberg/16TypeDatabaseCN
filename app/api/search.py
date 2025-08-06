from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.search_service import SearchService

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/")
def search_celebrities(
    q: str = Query(..., description="Search query"),
    search_type: str = Query(
        "all", description="Search type: all, name, description, tag, mbti"
    ),
    mbti_type: Optional[str] = Query(None, description="Filter by MBTI type"),
    tag_filter: Optional[str] = Query(None, description="Filter by tag"),
    popularity_filter: Optional[str] = Query(
        None, description="Filter by popularity: popular, recent, all"
    ),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of records to return"),
    db: Session = Depends(get_db),
):
    """
    Unified search endpoint with hybrid search and relevance scoring

    - **q**: Search query (required)
    - **search_type**: Type of search (all, name, description, tag, mbti)
    - **mbti_type**: Filter by MBTI type (optional)
    - **tag_filter**: Filter by tag (optional)
    - **popularity_filter**: Filter by popularity (popular, recent, all)
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Number of records to return (max 100)

    **Search Types:**
    - `all`: Hybrid search across all fields with relevance scoring
    - `name`: Search by celebrity name only
    - `description`: Search by description only
    - `tag`: Search by tags only
    - `mbti`: Search by MBTI type votes

    **Relevance Scoring:**
    - Exact name match: 100 points
    - Name contains: 80 points
    - Description contains: 60 points
    - Tag matches: 40 points
    """
    search_service = SearchService(db)

    # Validate search type
    valid_search_types = ["all", "name", "description", "tag", "mbti"]
    if search_type not in valid_search_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid search_type. Must be one of: {valid_search_types}",
        )

    # Validate popularity filter
    if popularity_filter and popularity_filter not in ["popular", "recent", "all"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid popularity_filter. Must be one of: popular, recent, all",
        )

    # Validate MBTI type if provided
    if mbti_type:
        valid_mbti_types = [
            "INTJ",
            "INTP",
            "ENTJ",
            "ENTP",
            "INFJ",
            "INFP",
            "ENFJ",
            "ENFP",
            "ISTJ",
            "ISFJ",
            "ESTJ",
            "ESFJ",
            "ISTP",
            "ISFP",
            "ESTP",
            "ESFP",
        ]
        if mbti_type.upper() not in valid_mbti_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid MBTI type. Must be one of: {valid_mbti_types}",
            )

    try:
        results = search_service.search_celebrities(
            query=q,
            search_type=search_type,
            mbti_type=mbti_type,
            tag_filter=tag_filter,
            popularity_filter=popularity_filter,
            skip=skip,
            limit=limit,
        )

        return {
            "query": q,
            "search_type": search_type,
            "total_results": len(results),
            "results": results,
            "pagination": {
                "skip": skip,
                "limit": limit,
                "has_more": len(results) == limit,
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search error: {str(e)}",
        )


@router.get("/suggestions")
def get_search_suggestions(
    q: str = Query(
        ..., min_length=2, description="Partial search query (minimum 2 characters)"
    ),
    limit: int = Query(10, ge=1, le=20, description="Number of suggestions to return"),
    db: Session = Depends(get_db),
):
    """
    Get search suggestions for autocomplete

    - **q**: Partial search query (minimum 2 characters)
    - **limit**: Number of suggestions to return (max 20)

    Returns suggestions from:
    - Celebrity names (Chinese and English)
    - Tag names
    """
    search_service = SearchService(db)

    try:
        suggestions = search_service.get_search_suggestions(q, limit)

        return {
            "query": q,
            "suggestions": suggestions,
            "total_suggestions": len(suggestions),
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting suggestions: {str(e)}",
        )


@router.get("/analytics")
def get_search_analytics(db: Session = Depends(get_db)):
    """
    Get search analytics and statistics

    Returns:
    - Total celebrities, tags, and votes
    - Popular tags with usage counts
    - Popular MBTI types with vote counts
    """
    search_service = SearchService(db)

    try:
        analytics = search_service.get_search_analytics()

        return {
            "statistics": analytics,
            "search_capabilities": {
                "search_types": ["all", "name", "description", "tag", "mbti"],
                "filters": ["mbti_type", "tag_filter", "popularity_filter"],
                "relevance_scoring": True,
                "autocomplete": True,
                "analytics": True,
            },
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting analytics: {str(e)}",
        )


@router.get("/mbti-types")
def get_mbti_types():
    """
    Get all available MBTI types for search filtering
    """
    mbti_types = [
        "INTJ",
        "INTP",
        "ENTJ",
        "ENTP",
        "INFJ",
        "INFP",
        "ENFJ",
        "ENFP",
        "ISTJ",
        "ISFJ",
        "ESTJ",
        "ESFJ",
        "ISTP",
        "ISFP",
        "ESTP",
        "ESFP",
    ]

    return {
        "mbti_types": mbti_types,
        "total_types": len(mbti_types),
        "description": "All 16 MBTI personality types available for search filtering",
    }


@router.get("/popular-searches")
def get_popular_searches(
    limit: int = Query(
        10, ge=1, le=50, description="Number of popular searches to return"
    ),
    db: Session = Depends(get_db),
):
    """
    Get popular search terms and trends

    - **limit**: Number of popular searches to return (max 50)

    Note: This endpoint can be enhanced in the future to track actual search queries
    """
    # For now, return sample popular searches based on existing data
    # In the future, this could be enhanced with actual search query tracking

    search_service = SearchService(db)
    analytics = search_service.get_search_analytics()

    # Generate popular searches based on popular tags and MBTI types
    popular_searches = []

    # Add popular tags as search suggestions
    for tag_data in analytics["popular_tags"][: limit // 2]:
        popular_searches.append(
            {"term": tag_data["tag"], "type": "tag", "count": tag_data["count"]}
        )

    # Add popular MBTI types as search suggestions
    for mbti_data in analytics["popular_mbti_types"][: limit // 2]:
        popular_searches.append(
            {"term": mbti_data["type"], "type": "mbti", "count": mbti_data["count"]}
        )

    # Sort by count and limit
    popular_searches.sort(key=lambda x: x["count"], reverse=True)
    popular_searches = popular_searches[:limit]

    return {
        "popular_searches": popular_searches,
        "total_searches": len(popular_searches),
        "note": (
            "Based on tag usage and MBTI vote counts. "
            "Future versions will track actual search queries."
        ),
    }
