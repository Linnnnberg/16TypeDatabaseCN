from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    Boolean,
    ForeignKey,
    Date,
    Enum as SQLEnum,
    Index,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum
import uuid

Base = declarative_base()


class UserRole(str, Enum):
    SYSTEM = "SYSTEM"
    CLIENT = "CLIENT"


class MBTIType(str, Enum):
    INTJ = "INTJ"
    INTP = "INTP"
    ENTJ = "ENTJ"
    ENTP = "ENTP"
    INFJ = "INFJ"
    INFP = "INFP"
    ENFJ = "ENFJ"
    ENFP = "ENFP"
    ISTJ = "ISTJ"
    ISFJ = "ISFJ"
    ESTJ = "ESTJ"
    ESFJ = "ESFJ"
    ISTP = "ISTP"
    ISFP = "ISFP"
    ESTP = "ESTP"
    ESFP = "ESFP"


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.CLIENT)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    votes = relationship("Vote", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    daily_stats = relationship("DailyUserStats", back_populates="user")


class Celebrity(Base):
    __tablename__ = "celebrities"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, index=True)
    name_en = Column(String)
    description = Column(Text)
    image_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    votes = relationship("Vote", back_populates="celebrity")
    comments = relationship("Comment", back_populates="celebrity")
    tags = relationship("CelebrityTag", back_populates="celebrity")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关系
    celebrities = relationship("CelebrityTag", back_populates="tag")


class CelebrityTag(Base):
    __tablename__ = "celebrity_tags"

    celebrity_id = Column(String, ForeignKey("celebrities.id"), primary_key=True)
    tag_id = Column(String, ForeignKey("tags.id"), primary_key=True)

    # 关系
    celebrity = relationship("Celebrity", back_populates="tags")
    tag = relationship("Tag", back_populates="celebrities")


class Vote(Base):
    __tablename__ = "votes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    celebrity_id = Column(String, ForeignKey("celebrities.id"), nullable=False)
    mbti_type = Column(SQLEnum(MBTIType), nullable=False)
    reason = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关系
    user = relationship("User", back_populates="votes")
    celebrity = relationship("Celebrity", back_populates="votes")

    # 唯一约束
    __table_args__ = (
        Index("ix_user_celebrity_vote", "user_id", "celebrity_id", unique=True),
    )


class Comment(Base):
    __tablename__ = "comments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    celebrity_id = Column(String, ForeignKey("celebrities.id"), nullable=False)
    content = Column(Text, nullable=False)
    parent_id = Column(String, ForeignKey("comments.id"))
    level = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    user = relationship("User", back_populates="comments")
    celebrity = relationship("Celebrity", back_populates="comments")
    parent = relationship("Comment", remote_side=[id])
    replies = relationship("Comment", back_populates="parent")


class DailyUserStats(Base):
    __tablename__ = "daily_user_stats"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    votes_count = Column(Integer, default=0)
    votes_no_reason = Column(Integer, default=0)

    # 关系
    user = relationship("User", back_populates="daily_stats")

    # 唯一约束
    __table_args__ = (Index("ix_user_date_stats", "user_id", "date", unique=True),)
