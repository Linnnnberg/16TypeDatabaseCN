from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from datetime import date
from fastapi import HTTPException, status
from app.database.models import Vote, User, Celebrity, DailyUserStats, MBTIType
from app.schemas.vote import VoteCreate


class VoteService:
    def __init__(self, db: Session):
        self.db = db

    def create_vote(self, user_id: str, vote_data: VoteCreate) -> Vote:
        """Create a new vote for a celebrity"""
        # Check if celebrity exists
        celebrity = (
            self.db.query(Celebrity)
            .filter(Celebrity.id == vote_data.celebrity_id)
            .first()
        )
        if not celebrity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Celebrity not found"
            )

        # Check if user has already voted for this celebrity
        existing_vote = (
            self.db.query(Vote)
            .filter(
                and_(
                    Vote.user_id == user_id, Vote.celebrity_id == vote_data.celebrity_id
                )
            )
            .first()
        )

        if existing_vote:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already voted for this celebrity",
            )

        # Check daily vote limit (max 10 votes per day)
        today = date.today()
        daily_stats = (
            self.db.query(DailyUserStats)
            .filter(
                and_(DailyUserStats.user_id == user_id, DailyUserStats.date == today)
            )
            .first()
        )

        if daily_stats and daily_stats.votes_count >= 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Daily vote limit reached (10 votes per day)",
            )

        # Create the vote
        vote = Vote(
            user_id=user_id,
            celebrity_id=vote_data.celebrity_id,
            mbti_type=vote_data.mbti_type,
            reason=vote_data.reason,
        )

        self.db.add(vote)

        # Update or create daily stats
        if daily_stats:
            daily_stats.votes_count += 1
            if not vote_data.reason:
                daily_stats.votes_no_reason += 1
        else:
            daily_stats = DailyUserStats(
                user_id=user_id,
                date=today,
                votes_count=1,
                votes_no_reason=1 if not vote_data.reason else 0,
            )
            self.db.add(daily_stats)

        self.db.commit()
        self.db.refresh(vote)

        return vote

    def get_vote_by_id(self, vote_id: str) -> Optional[Vote]:
        """Get vote by ID"""
        return self.db.query(Vote).filter(Vote.id == vote_id).first()

    def get_user_votes(
        self, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[Vote]:
        """Get all votes by a user"""
        return (
            self.db.query(Vote)
            .filter(Vote.user_id == user_id)
            .order_by(Vote.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_celebrity_votes(
        self, celebrity_id: str, skip: int = 0, limit: int = 100
    ) -> List[Vote]:
        """Get all votes for a celebrity"""
        return (
            self.db.query(Vote)
            .filter(Vote.celebrity_id == celebrity_id)
            .order_by(Vote.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_all_votes(
        self,
        skip: int = 0,
        limit: int = 100,
        celebrity_id: Optional[str] = None,
        user_id: Optional[str] = None,
        mbti_type: Optional[MBTIType] = None,
    ) -> List[Vote]:
        """Get all votes with optional filters"""
        query = self.db.query(Vote)

        if celebrity_id:
            query = query.filter(Vote.celebrity_id == celebrity_id)
        if user_id:
            query = query.filter(Vote.user_id == user_id)
        if mbti_type:
            query = query.filter(Vote.mbti_type == mbti_type)

        return query.order_by(Vote.created_at.desc()).offset(skip).limit(limit).all()

    def delete_vote(self, vote_id: str, user_id: str) -> bool:
        """Delete a vote (only by the user who created it)"""
        vote = self.get_vote_by_id(vote_id)
        if not vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found"
            )

        if vote.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete your own votes",
            )

        # Update daily stats
        vote_date = vote.created_at.date()
        daily_stats = (
            self.db.query(DailyUserStats)
            .filter(
                and_(
                    DailyUserStats.user_id == user_id, DailyUserStats.date == vote_date
                )
            )
            .first()
        )

        if daily_stats:
            daily_stats.votes_count -= 1
            if not vote.reason:
                daily_stats.votes_no_reason -= 1

            # Remove daily stats if no votes left
            if daily_stats.votes_count <= 0:
                self.db.delete(daily_stats)

        self.db.delete(vote)
        self.db.commit()

        return True

    def get_celebrity_vote_statistics(self, celebrity_id: str) -> Dict[str, Any]:
        """Get vote statistics for a celebrity"""
        # Check if celebrity exists
        celebrity = (
            self.db.query(Celebrity).filter(Celebrity.id == celebrity_id).first()
        )
        if not celebrity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Celebrity not found"
            )

        # Get total votes count
        total_votes = (
            self.db.query(func.count(Vote.id))
            .filter(Vote.celebrity_id == celebrity_id)
            .scalar()
        )

        # Get votes by MBTI type
        mbti_counts = (
            self.db.query(Vote.mbti_type, func.count(Vote.id).label("count"))
            .filter(Vote.celebrity_id == celebrity_id)
            .group_by(Vote.mbti_type)
            .order_by(desc("count"))
            .all()
        )

        # Get votes with reasons vs without reasons
        votes_with_reason = (
            self.db.query(func.count(Vote.id))
            .filter(and_(Vote.celebrity_id == celebrity_id, Vote.reason.isnot(None)))
            .scalar()
        )

        votes_without_reason = total_votes - votes_with_reason

        return {
            "celebrity_id": celebrity_id,
            "celebrity_name": celebrity.name,
            "total_votes": total_votes,
            "votes_with_reason": votes_with_reason,
            "votes_without_reason": votes_without_reason,
            "mbti_distribution": [
                {
                    "mbti_type": mbti_type.value,
                    "count": count,
                    "percentage": (
                        round((count / total_votes * 100), 2) if total_votes > 0 else 0
                    ),
                }
                for mbti_type, count in mbti_counts
            ],
            "top_mbti_type": mbti_counts[0][0].value if mbti_counts else None,
            "top_mbti_count": mbti_counts[0][1] if mbti_counts else 0,
        }

    def get_user_vote_statistics(self, user_id: str) -> Dict[str, Any]:
        """Get vote statistics for a user"""
        # Check if user exists
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        # Get total votes count
        total_votes = (
            self.db.query(func.count(Vote.id)).filter(Vote.user_id == user_id).scalar()
        )

        # Get votes by MBTI type
        mbti_counts = (
            self.db.query(Vote.mbti_type, func.count(Vote.id).label("count"))
            .filter(Vote.user_id == user_id)
            .group_by(Vote.mbti_type)
            .order_by(desc("count"))
            .all()
        )

        # Get today's votes
        today = date.today()
        today_votes = (
            self.db.query(func.count(Vote.id))
            .filter(and_(Vote.user_id == user_id, func.date(Vote.created_at) == today))
            .scalar()
        )

        # Get daily stats
        daily_stats = (
            self.db.query(DailyUserStats)
            .filter(DailyUserStats.user_id == user_id)
            .order_by(DailyUserStats.date.desc())
            .limit(7)
            .all()
        )  # Last 7 days

        return {
            "user_id": user_id,
            "user_name": user.name,
            "total_votes": total_votes,
            "today_votes": today_votes,
            "votes_remaining_today": max(0, 10 - today_votes),
            "mbti_distribution": [
                {
                    "mbti_type": mbti_type.value,
                    "count": count,
                    "percentage": (
                        round((count / total_votes * 100), 2) if total_votes > 0 else 0
                    ),
                }
                for mbti_type, count in mbti_counts
            ],
            "favorite_mbti_type": mbti_counts[0][0].value if mbti_counts else None,
            "favorite_mbti_count": mbti_counts[0][1] if mbti_counts else 0,
            "recent_daily_stats": [
                {
                    "date": stats.date.isoformat(),
                    "votes_count": stats.votes_count,
                    "votes_no_reason": stats.votes_no_reason,
                }
                for stats in daily_stats
            ],
        }

    def get_popular_celebrities_by_votes(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get celebrities ordered by number of votes"""
        celebrities = (
            self.db.query(Celebrity, func.count(Vote.id).label("vote_count"))
            .outerjoin(Vote)
            .group_by(Celebrity.id)
            .order_by(desc("vote_count"))
            .limit(limit)
            .all()
        )

        return [
            {
                "celebrity": celebrity,
                "vote_count": vote_count,
                "top_mbti": self._get_celebrity_top_mbti(celebrity.id),
            }
            for celebrity, vote_count in celebrities
        ]

    def _get_celebrity_top_mbti(self, celebrity_id: str) -> Optional[str]:
        """Get the most voted MBTI type for a celebrity"""
        result = (
            self.db.query(Vote.mbti_type, func.count(Vote.id).label("count"))
            .filter(Vote.celebrity_id == celebrity_id)
            .group_by(Vote.mbti_type)
            .order_by(desc("count"))
            .first()
        )

        return result[0].value if result else None
