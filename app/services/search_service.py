from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func, desc, case, text
from fastapi import HTTPException, status
from app.database.models import Celebrity, Tag, CelebrityTag, Vote, MBTIType
from app.schemas.celebrity import CelebrityResponse


class SearchResult:
    def __init__(self, celebrity: Celebrity, relevance_score: float, match_type: str):
        self.celebrity = celebrity
        self.relevance_score = relevance_score
        self.match_type = match_type


class SearchService:
    def __init__(self, db: Session):
        self.db = db

    def search_celebrities(
        self,
        query: str,
        search_type: str = "all",
        mbti_type: Optional[str] = None,
        tag_filter: Optional[str] = None,
        popularity_filter: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        Hybrid search with relevance scoring

        Args:
            query: Search query string
            search_type: Type of search (all, name, description, tag, mbti)
            mbti_type: Filter by MBTI type
            tag_filter: Filter by tag
            popularity_filter: Filter by popularity (popular, recent, all)
            skip: Number of records to skip
            limit: Number of records to return
        """
        if not query.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Search query cannot be empty",
            )

        # Build base query
        base_query = self.db.query(Celebrity)

        # Apply filters
        if mbti_type:
            base_query = self._apply_mbti_filter(base_query, mbti_type)

        if tag_filter:
            base_query = self._apply_tag_filter(base_query, tag_filter)

        if popularity_filter:
            base_query = self._apply_popularity_filter(base_query, popularity_filter)

        # Apply search based on type
        if search_type == "name":
            results = self._search_by_name(base_query, query, skip, limit)
        elif search_type == "description":
            results = self._search_by_description(base_query, query, skip, limit)
        elif search_type == "tag":
            results = self._search_by_tag(base_query, query, skip, limit)
        elif search_type == "mbti":
            results = self._search_by_mbti(base_query, query, skip, limit)
        else:  # "all"
            results = self._hybrid_search(base_query, query, skip, limit)

        return results

    def _hybrid_search(
        self, base_query, query: str, skip: int, limit: int
    ) -> List[Dict[str, Any]]:
        """Hybrid search with relevance scoring"""
        query_lower = query.lower()

        # Build complex query with relevance scoring
        search_query = (
            base_query.add_columns(
                # Relevance scoring
                case(
                    # Exact name match (highest priority)
                    (func.lower(Celebrity.name) == query_lower, 100),
                    (func.lower(Celebrity.name_en) == query_lower, 100),
                    # Name contains (high priority)
                    (func.lower(Celebrity.name).contains(query_lower), 80),
                    (func.lower(Celebrity.name_en).contains(query_lower), 80),
                    # Description contains (medium priority)
                    (func.lower(Celebrity.description).contains(query_lower), 60),
                    # Tag matches (lower priority)
                    (
                        func.lower(Celebrity.tags.any(Tag.name.contains(query_lower))),
                        40,
                    ),
                    # Default score
                    else_=0,
                ).label("relevance_score")
            )
            .filter(
                or_(
                    func.lower(Celebrity.name).contains(query_lower),
                    func.lower(Celebrity.name_en).contains(query_lower),
                    func.lower(Celebrity.description).contains(query_lower),
                    Celebrity.tags.any(Tag.name.contains(query_lower)),
                )
            )
            .order_by(desc("relevance_score"), desc(Celebrity.created_at))
        )

        # Execute query with pagination
        results = search_query.offset(skip).limit(limit).all()

        # Format results
        formatted_results = []
        for celebrity, relevance_score in results:
            result = CelebrityResponse.model_validate(celebrity).model_dump()
            result["relevance_score"] = relevance_score or 0
            result["match_type"] = self._determine_match_type(
                query_lower, celebrity, relevance_score
            )
            formatted_results.append(result)

        return formatted_results

    def _search_by_name(
        self, base_query, query: str, skip: int, limit: int
    ) -> List[Dict[str, Any]]:
        """Search by celebrity name only"""
        query_lower = query.lower()

        search_query = (
            base_query.add_columns(
                case(
                    (func.lower(Celebrity.name) == query_lower, 100),
                    (func.lower(Celebrity.name_en) == query_lower, 100),
                    (func.lower(Celebrity.name).contains(query_lower), 80),
                    (func.lower(Celebrity.name_en).contains(query_lower), 80),
                    else_=0,
                ).label("relevance_score")
            )
            .filter(
                or_(
                    func.lower(Celebrity.name).contains(query_lower),
                    func.lower(Celebrity.name_en).contains(query_lower),
                )
            )
            .order_by(desc("relevance_score"), desc(Celebrity.created_at))
        )

        results = search_query.offset(skip).limit(limit).all()

        formatted_results = []
        for celebrity, relevance_score in results:
            result = CelebrityResponse.model_validate(celebrity).model_dump()
            result["relevance_score"] = relevance_score or 0
            result["match_type"] = "name_match"
            formatted_results.append(result)

        return formatted_results

    def _search_by_description(
        self, base_query, query: str, skip: int, limit: int
    ) -> List[Dict[str, Any]]:
        """Search by description only"""
        query_lower = query.lower()

        search_query = (
            base_query.add_columns(
                case(
                    (func.lower(Celebrity.description).contains(query_lower), 60),
                    else_=0,
                ).label("relevance_score")
            )
            .filter(func.lower(Celebrity.description).contains(query_lower))
            .order_by(desc("relevance_score"), desc(Celebrity.created_at))
        )

        results = search_query.offset(skip).limit(limit).all()

        formatted_results = []
        for celebrity, relevance_score in results:
            result = CelebrityResponse.model_validate(celebrity).model_dump()
            result["relevance_score"] = relevance_score or 0
            result["match_type"] = "description_match"
            formatted_results.append(result)

        return formatted_results

    def _search_by_tag(
        self, base_query, query: str, skip: int, limit: int
    ) -> List[Dict[str, Any]]:
        """Search by tag only"""
        query_lower = query.lower()

        search_query = (
            base_query.add_columns(
                case(
                    (
                        func.lower(Celebrity.tags.any(Tag.name.contains(query_lower))),
                        40,
                    ),
                    else_=0,
                ).label("relevance_score")
            )
            .filter(Celebrity.tags.any(Tag.name.contains(query_lower)))
            .order_by(desc("relevance_score"), desc(Celebrity.created_at))
        )

        results = search_query.offset(skip).limit(limit).all()

        formatted_results = []
        for celebrity, relevance_score in results:
            result = CelebrityResponse.model_validate(celebrity).model_dump()
            result["relevance_score"] = relevance_score or 0
            result["match_type"] = "tag_match"
            formatted_results.append(result)

        return formatted_results

    def _search_by_mbti(
        self, base_query, query: str, skip: int, limit: int
    ) -> List[Dict[str, Any]]:
        """Search by MBTI type votes"""
        query_upper = query.upper()

        # Get celebrities with votes for the specified MBTI type
        search_query = (
            base_query.add_columns(func.count(Vote.id).label("vote_count_for_type"))
            .join(Vote, Celebrity.id == Vote.celebrity_id)
            .filter(Vote.mbti_type == query_upper)
            .group_by(Celebrity.id)
            .order_by(desc("vote_count_for_type"))
        )

        results = search_query.offset(skip).limit(limit).all()

        formatted_results = []
        for celebrity, vote_count in results:
            result = CelebrityResponse.model_validate(celebrity).model_dump()
            result["relevance_score"] = vote_count or 0
            result["match_type"] = "mbti_match"
            formatted_results.append(result)

        return formatted_results

    def _apply_mbti_filter(self, query, mbti_type: str):
        """Apply MBTI type filter"""
        return (
            query.join(Vote, Celebrity.id == Vote.celebrity_id)
            .filter(Vote.mbti_type == mbti_type.upper())
            .group_by(Celebrity.id)
        )

    def _apply_tag_filter(self, query, tag_name: str):
        """Apply tag filter"""
        return query.filter(Celebrity.tags.any(Tag.name.contains(tag_name)))

    def _apply_popularity_filter(self, query, popularity_filter: str):
        """Apply popularity filter"""
        if popularity_filter == "popular":
            # Order by vote count using subquery
            return (
                query.add_columns(func.count(Vote.id).label("vote_count"))
                .outerjoin(Vote, Celebrity.id == Vote.celebrity_id)
                .group_by(Celebrity.id)
                .order_by(desc("vote_count"))
            )
        elif popularity_filter == "recent":
            return query.order_by(desc(Celebrity.created_at))
        else:  # "all"
            return query

    def _determine_match_type(
        self, query_lower: str, celebrity: Celebrity, relevance_score: float
    ) -> str:
        """Determine the type of match for the celebrity"""
        if relevance_score >= 100:
            return "exact_match"
        elif relevance_score >= 80:
            return "name_contains"
        elif relevance_score >= 60:
            return "description_match"
        elif relevance_score >= 40:
            return "tag_match"
        else:
            return "partial_match"

    def get_search_suggestions(self, query: str, limit: int = 10) -> List[str]:
        """Get search suggestions based on partial query"""
        if len(query.strip()) < 2:
            return []

        query_lower = query.lower()

        # Get celebrity name suggestions
        name_suggestions = (
            self.db.query(Celebrity.name)
            .filter(func.lower(Celebrity.name).contains(query_lower))
            .limit(limit // 2)
            .all()
        )

        # Get English name suggestions
        name_en_suggestions = (
            self.db.query(Celebrity.name_en)
            .filter(func.lower(Celebrity.name_en).contains(query_lower))
            .limit(limit // 2)
            .all()
        )

        # Get tag suggestions
        tag_suggestions = (
            self.db.query(Tag.name)
            .filter(func.lower(Tag.name).contains(query_lower))
            .limit(limit // 4)
            .all()
        )

        # Combine and deduplicate suggestions
        all_suggestions = []
        for suggestion in name_suggestions + name_en_suggestions + tag_suggestions:
            if suggestion[0] and suggestion[0].lower() not in [
                s.lower() for s in all_suggestions
            ]:
                all_suggestions.append(suggestion[0])

        return all_suggestions[:limit]

    def get_search_analytics(self) -> Dict[str, Any]:
        """Get search analytics and statistics"""
        total_celebrities = self.db.query(Celebrity).count()
        total_tags = self.db.query(Tag).count()
        total_votes = self.db.query(Vote).count()

        # Get popular tags
        popular_tags = (
            self.db.query(
                Tag.name, func.count(CelebrityTag.celebrity_id).label("usage_count")
            )
            .join(CelebrityTag, Tag.id == CelebrityTag.tag_id)
            .group_by(Tag.id)
            .order_by(desc("usage_count"))
            .limit(10)
            .all()
        )

        # Get popular MBTI types
        popular_mbti = (
            self.db.query(Vote.mbti_type, func.count(Vote.id).label("vote_count"))
            .group_by(Vote.mbti_type)
            .order_by(desc("vote_count"))
            .all()
        )

        return {
            "total_celebrities": total_celebrities,
            "total_tags": total_tags,
            "total_votes": total_votes,
            "popular_tags": [
                {"tag": tag, "count": count} for tag, count in popular_tags
            ],
            "popular_mbti_types": [
                {"type": mbti_type, "count": count} for mbti_type, count in popular_mbti
            ],
        }
