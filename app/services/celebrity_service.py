from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status
from app.database.models import Celebrity, Tag, CelebrityTag
from app.schemas.celebrity import CelebrityCreate, CelebrityUpdate


class CelebrityService:
    def __init__(self, db: Session):
        self.db = db

    def create_celebrity(self, celebrity_data: CelebrityCreate) -> Celebrity:
        """Create a new celebrity"""
        # Check if celebrity with same name already exists
        existing_celebrity = (
            self.db.query(Celebrity)
            .filter(
                or_(
                    Celebrity.name == celebrity_data.name,
                    Celebrity.name_en == celebrity_data.name_en,
                )
            )
            .first()
        )

        if existing_celebrity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Celebrity with this name already exists",
            )

        # Create new celebrity
        celebrity = Celebrity(
            name=celebrity_data.name,
            name_en=celebrity_data.name_en,
            description=celebrity_data.description,
            image_url=celebrity_data.image_url,
        )

        self.db.add(celebrity)
        self.db.commit()
        self.db.refresh(celebrity)

        return celebrity

    def get_celebrity_by_id(self, celebrity_id: str) -> Optional[Celebrity]:
        """Get celebrity by ID"""
        return self.db.query(Celebrity).filter(Celebrity.id == celebrity_id).first()

    def get_celebrity_by_name(self, name: str) -> Optional[Celebrity]:
        """Get celebrity by name (Chinese or English)"""
        return (
            self.db.query(Celebrity)
            .filter(or_(Celebrity.name == name, Celebrity.name_en == name))
            .first()
        )

    def get_all_celebrities(
        self, skip: int = 0, limit: int = 100, search: Optional[str] = None
    ) -> List[Celebrity]:
        """Get all celebrities with optional search and pagination"""
        query = self.db.query(Celebrity)

        if search:
            query = query.filter(
                or_(
                    Celebrity.name.contains(search),
                    Celebrity.name_en.contains(search),
                    Celebrity.description.contains(search),
                )
            )

        return query.offset(skip).limit(limit).all()

    def update_celebrity(
        self, celebrity_id: str, celebrity_data: CelebrityUpdate
    ) -> Celebrity:
        """Update celebrity information"""
        celebrity = self.get_celebrity_by_id(celebrity_id)
        if not celebrity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Celebrity not found"
            )

        # Check for name conflicts if name is being updated
        if celebrity_data.name and celebrity_data.name != celebrity.name:
            existing = self.get_celebrity_by_name(celebrity_data.name)
            if existing and existing.id != celebrity_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Celebrity with this name already exists",
                )

        # Update fields if provided
        if celebrity_data.name is not None:
            celebrity.name = celebrity_data.name
        if celebrity_data.name_en is not None:
            celebrity.name_en = celebrity_data.name_en
        if celebrity_data.description is not None:
            celebrity.description = celebrity_data.description
        if celebrity_data.image_url is not None:
            celebrity.image_url = celebrity_data.image_url

        self.db.commit()
        self.db.refresh(celebrity)

        return celebrity

    def delete_celebrity(self, celebrity_id: str) -> bool:
        """Delete a celebrity"""
        celebrity = self.get_celebrity_by_id(celebrity_id)
        if not celebrity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Celebrity not found"
            )

        # Check if celebrity has votes or comments
        if celebrity.votes or celebrity.comments:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete celebrity with existing votes or comments",
            )

        self.db.delete(celebrity)
        self.db.commit()

        return True

    def add_tag_to_celebrity(self, celebrity_id: str, tag_name: str) -> CelebrityTag:
        """Add a tag to a celebrity"""
        celebrity = self.get_celebrity_by_id(celebrity_id)
        if not celebrity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Celebrity not found"
            )

        # Get or create tag
        tag = self.db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            self.db.add(tag)
            self.db.commit()
            self.db.refresh(tag)

        # Check if tag is already assigned
        existing_tag = (
            self.db.query(CelebrityTag)
            .filter(
                CelebrityTag.celebrity_id == celebrity_id, CelebrityTag.tag_id == tag.id
            )
            .first()
        )

        if existing_tag:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tag already assigned to this celebrity",
            )

        # Create celebrity tag relationship
        celebrity_tag = CelebrityTag(celebrity_id=celebrity_id, tag_id=tag.id)

        self.db.add(celebrity_tag)
        self.db.commit()
        self.db.refresh(celebrity_tag)

        return celebrity_tag

    def remove_tag_from_celebrity(self, celebrity_id: str, tag_name: str) -> bool:
        """Remove a tag from a celebrity"""
        celebrity = self.get_celebrity_by_id(celebrity_id)
        if not celebrity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Celebrity not found"
            )

        tag = self.db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
            )

        celebrity_tag = (
            self.db.query(CelebrityTag)
            .filter(
                CelebrityTag.celebrity_id == celebrity_id, CelebrityTag.tag_id == tag.id
            )
            .first()
        )

        if not celebrity_tag:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tag not assigned to this celebrity",
            )

        self.db.delete(celebrity_tag)
        self.db.commit()

        return True

    def get_celebrities_by_tag(
        self, tag_name: str, skip: int = 0, limit: int = 100
    ) -> List[Celebrity]:
        """Get celebrities by tag"""
        tag = self.db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            return []

        celebrities = (
            self.db.query(Celebrity)
            .join(CelebrityTag)
            .filter(CelebrityTag.tag_id == tag.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

        return celebrities

    def get_popular_celebrities(self, limit: int = 10) -> List[Celebrity]:
        """Get celebrities with most votes"""
        from sqlalchemy import func

        celebrities = (
            self.db.query(Celebrity, func.count(Celebrity.votes).label("vote_count"))
            .outerjoin(Celebrity.votes)
            .group_by(Celebrity.id)
            .order_by(func.count(Celebrity.votes).desc())
            .limit(limit)
            .all()
        )

        # Extract just the celebrity objects from the result
        return [celebrity for celebrity, _ in celebrities]
