from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc, func
from app.database.models import Comment, Celebrity
from app.schemas.comment import CommentCreate
from fastapi import HTTPException, status
import uuid
from datetime import datetime


class CommentService:
    def __init__(self, db: Session):
        self.db = db

    def create_comment(self, user_id: str, comment_data: CommentCreate) -> Comment:
        """
        Create a new comment for a celebrity

        Args:
            user_id: ID of the user creating the comment
            comment_data: Comment data including celebrity_id, content, and optional
                parent_id

        Returns:
            Created comment object

        Raises:
            HTTPException: If celebrity doesn't exist or parent comment doesn't exist
        """
        # Verify celebrity exists
        celebrity = (
            self.db.query(Celebrity)
            .filter(Celebrity.id == comment_data.celebrity_id)
            .first()
        )
        if not celebrity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Celebrity not found"
            )

        # If this is a reply, verify parent comment exists and belongs to same celebrity
        level = 1
        if comment_data.parent_id:
            parent_comment = (
                self.db.query(Comment)
                .filter(
                    and_(
                        Comment.id == comment_data.parent_id,
                        Comment.celebrity_id == comment_data.celebrity_id,
                    )
                )
                .first()
            )

            if not parent_comment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=(
                        "Parent comment not found or doesn't belong to this celebrity"
                    ),
                )

            # Set level based on parent (max 3 levels deep)
            level = min(parent_comment.level + 1, 3)

        # Create the comment
        comment = Comment(
            id=str(uuid.uuid4()),
            user_id=user_id,
            celebrity_id=comment_data.celebrity_id,
            content=comment_data.content,
            parent_id=comment_data.parent_id,
            level=level,
        )

        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)

        return comment

    def get_comment_by_id(self, comment_id: str) -> Optional[Comment]:
        """
        Get a specific comment by ID

        Args:
            comment_id: ID of the comment

        Returns:
            Comment object or None if not found
        """
        return self.db.query(Comment).filter(Comment.id == comment_id).first()

    def get_celebrity_comments(
        self,
        celebrity_id: str,
        skip: int = 0,
        limit: int = 100,
        include_replies: bool = True,
    ) -> List[Comment]:
        """
        Get all comments for a celebrity

        Args:
            celebrity_id: ID of the celebrity
            skip: Number of records to skip
            limit: Number of records to return
            include_replies: Whether to include reply comments

        Returns:
            List of comments
        """
        query = self.db.query(Comment).filter(Comment.celebrity_id == celebrity_id)

        if not include_replies:
            # Only top-level comments (no parent_id)
            query = query.filter(Comment.parent_id.is_(None))

        return query.order_by(desc(Comment.created_at)).offset(skip).limit(limit).all()

    def get_user_comments(
        self, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[Comment]:
        """
        Get all comments by a specific user

        Args:
            user_id: ID of the user
            skip: Number of records to skip
            limit: Number of records to return

        Returns:
            List of comments
        """
        return (
            self.db.query(Comment)
            .filter(Comment.user_id == user_id)
            .order_by(desc(Comment.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_comment_replies(
        self, comment_id: str, skip: int = 0, limit: int = 50
    ) -> List[Comment]:
        """
        Get all replies to a specific comment

        Args:
            comment_id: ID of the parent comment
            skip: Number of records to skip
            limit: Number of records to return

        Returns:
            List of reply comments
        """
        return (
            self.db.query(Comment)
            .filter(Comment.parent_id == comment_id)
            .order_by(Comment.created_at)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_comment(self, comment_id: str, user_id: str, content: str) -> Comment:
        """
        Update a comment (only by the user who created it)

        Args:
            comment_id: ID of the comment to update
            user_id: ID of the user making the update
            content: New comment content

        Returns:
            Updated comment object

        Raises:
            HTTPException: If comment doesn't exist or user doesn't own it
        """
        comment = (
            self.db.query(Comment)
            .filter(and_(Comment.id == comment_id, Comment.user_id == user_id))
            .first()
        )

        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found or you don't have permission to edit it",
            )

        comment.content = content
        comment.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(comment)

        return comment

    def delete_comment(self, comment_id: str, user_id: str) -> None:
        """
        Delete a comment (only by the user who created it)

        Args:
            comment_id: ID of the comment to delete
            user_id: ID of the user making the deletion

        Raises:
            HTTPException: If comment doesn't exist or user doesn't own it
        """
        comment = (
            self.db.query(Comment)
            .filter(and_(Comment.id == comment_id, Comment.user_id == user_id))
            .first()
        )

        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found or you don't have permission to delete it",
            )

        # Check if comment has replies
        replies_count = (
            self.db.query(Comment).filter(Comment.parent_id == comment_id).count()
        )
        if replies_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Cannot delete comment with replies. Please delete replies first."
                ),
            )

        self.db.delete(comment)
        self.db.commit()

    def get_comment_statistics(self, celebrity_id: str) -> Dict[str, Any]:
        """
        Get comment statistics for a celebrity

        Args:
            celebrity_id: ID of the celebrity

        Returns:
            Dictionary with comment statistics
        """
        # Total comments
        total_comments = (
            self.db.query(Comment).filter(Comment.celebrity_id == celebrity_id).count()
        )

        # Top-level comments
        top_level_comments = (
            self.db.query(Comment)
            .filter(
                and_(Comment.celebrity_id == celebrity_id, Comment.parent_id.is_(None))
            )
            .count()
        )

        # Reply comments
        reply_comments = (
            self.db.query(Comment)
            .filter(
                and_(
                    Comment.celebrity_id == celebrity_id, Comment.parent_id.is_not(None)
                )
            )
            .count()
        )

        # Most active commenters
        active_commenters = (
            self.db.query(
                Comment.user_id, func.count(Comment.id).label("comment_count")
            )
            .filter(Comment.celebrity_id == celebrity_id)
            .group_by(Comment.user_id)
            .order_by(desc("comment_count"))
            .limit(5)
            .all()
        )

        return {
            "total_comments": total_comments,
            "top_level_comments": top_level_comments,
            "reply_comments": reply_comments,
            "active_commenters": [
                {"user_id": user_id, "comment_count": count}
                for user_id, count in active_commenters
            ],
        }

    def get_user_comment_statistics(self, user_id: str) -> Dict[str, Any]:
        """
        Get comment statistics for a user

        Args:
            user_id: ID of the user

        Returns:
            Dictionary with user comment statistics
        """
        # Total comments by user
        total_comments = (
            self.db.query(Comment).filter(Comment.user_id == user_id).count()
        )

        # Top-level comments
        top_level_comments = (
            self.db.query(Comment)
            .filter(and_(Comment.user_id == user_id, Comment.parent_id.is_(None)))
            .count()
        )

        # Reply comments
        reply_comments = (
            self.db.query(Comment)
            .filter(and_(Comment.user_id == user_id, Comment.parent_id.is_not(None)))
            .count()
        )

        # Recent comments (last 7 days)
        recent_comments = (
            self.db.query(Comment)
            .filter(
                and_(
                    Comment.user_id == user_id,
                    Comment.created_at
                    >= datetime.utcnow().replace(
                        hour=0, minute=0, second=0, microsecond=0
                    ),
                )
            )
            .count()
        )

        return {
            "total_comments": total_comments,
            "top_level_comments": top_level_comments,
            "reply_comments": reply_comments,
            "recent_comments": recent_comments,
        }
