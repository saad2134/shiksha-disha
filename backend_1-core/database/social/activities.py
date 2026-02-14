"""Social activity feed models."""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database.core.base import BaseModel


class SocialActivity(BaseModel):
    """Social activities for activity feeds."""
    __tablename__ = "social_activities"
    
    # Actor
    actor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Activity details
    activity_type = Column(String(50), nullable=False)  # streak_achieved, badge_earned, course_completed, duel_won
    action_verb = Column(String(50), nullable=False)  # achieved, earned, completed, won
    
    # Object
    object_type = Column(String(50), nullable=True)  # streak, badge, course, duel
    object_id = Column(Integer, nullable=True)
    object_name = Column(String(200), nullable=True)  # "7-Day Streak", "Python Expert Badge"
    
    # Context
    target_id = Column(Integer, nullable=True)  # If directed at someone (duel opponent)
    target_type = Column(String(50), nullable=True)
    
    # Content
    content = Column(Text, nullable=True)  # Formatted activity text
    metadata = Column(JSON, nullable=True)  # Additional context
    
    # Media
    image_url = Column(String(500), nullable=True)
    
    # Privacy
    is_public = Column(Boolean, default=True)
    visible_to = Column(JSON, nullable=True)  # NULL = public, [] = private, [user_ids]
    
    # Engagement
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    actor = relationship("User")
    likes = relationship("ActivityLike", back_populates="activity", cascade="all, delete-orphan")
    comments = relationship("ActivityComment", back_populates="activity", cascade="all, delete-orphan")


class ActivityLike(BaseModel):
    """Likes on social activities."""
    __tablename__ = "activity_likes"
    
    activity_id = Column(Integer, ForeignKey("social_activities.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    activity = relationship("SocialActivity", back_populates="likes")
    user = relationship("User")


class ActivityComment(BaseModel):
    """Comments on social activities."""
    __tablename__ = "activity_comments"
    
    activity_id = Column(Integer, ForeignKey("social_activities.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    content = Column(Text, nullable=False)
    
    # Engagement
    likes_count = Column(Integer, default=0)
    
    # Threading
    parent_comment_id = Column(Integer, ForeignKey("activity_comments.id"), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
    
    # Relationships
    activity = relationship("SocialActivity", back_populates="comments")
    user = relationship("User")
    replies = relationship("ActivityComment", backref="parent", remote_side="ActivityComment.id")


class ActivityFeed(BaseModel):
    """Personalized activity feed cache."""
    __tablename__ = "activity_feeds"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("social_activities.id"), nullable=False)
    
    # Feed position
    position_score = Column(Float, nullable=False)  # For ranking
    
    # Status
    is_seen = Column(Boolean, default=False)
    seen_at = Column(DateTime, nullable=True)
    
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime, nullable=True)
    
    # Source
    source = Column(String(50), default="following")  # following, trending, recommended
    
    added_at = Column(DateTime, default=datetime.utcnow)
