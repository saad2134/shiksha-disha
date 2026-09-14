"""Badge and achievement models."""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database.core.base import BaseModel
from database.core.enums import BadgeCategory, BadgeRarity


class Badge(BaseModel):
    """Badge/achievement definitions."""
    __tablename__ = "badges"
    
    # Basic info
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    short_description = Column(String(255), nullable=True)
    
    # Visual
    icon_url = Column(String(500), nullable=False)
    icon_url_locked = Column(String(500), nullable=True)  # Grayscale version
    color_hex = Column(String(7), nullable=True)  # #RRGGBB
    
    # Categorization
    category = Column(Enum(BadgeCategory), nullable=False)
    rarity = Column(Enum(BadgeRarity), default=BadgeRarity.COMMON)
    
    # Unlock criteria
    criteria = Column(JSON, nullable=False)  # {"streak_days": 7, "courses_completed": 5}
    criteria_description = Column(Text, nullable=True)  # Human-readable
    
    # Metadata
    is_hidden = Column(Boolean, default=False)  # Secret badges
    is_limited = Column(Boolean, default=False)  # Limited time/event badges
    event_id = Column(Integer, nullable=True)  # If tied to event
    
    # Points reward
    points_reward = Column(Integer, default=0)
    
    # Relationships
    user_badges = relationship("UserBadge", back_populates="badge", cascade="all, delete-orphan")


class UserBadge(BaseModel):
    """User's earned badges."""
    __tablename__ = "user_badges"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=False)
    
    # Earned info
    earned_at = Column(DateTime, default=datetime.utcnow)
    earned_date = Column(Date, default=datetime.utcnow().date)
    
    # Progress tracking (if earned over time)
    progress_percentage = Column(Float, default=100.0)
    progress_details = Column(JSON, nullable=True)  # {"completed": 5, "required": 5}
    
    # Display
    is_showcased = Column(Boolean, default=False)  # On profile
    showcase_order = Column(Integer, nullable=True)
    is_new = Column(Boolean, default=True)  # Unseen notification
    seen_at = Column(DateTime, nullable=True)
    
    # Sharing
    shared_count = Column(Integer, default=0)
    last_shared_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="badges")
    badge = relationship("Badge", back_populates="user_badges")


class AchievementProgress(BaseModel):
    """Track progress toward badges/achievements."""
    __tablename__ = "achievement_progress"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=False)
    
    # Progress
    current_value = Column(Float, default=0.0)
    target_value = Column(Float, nullable=False)
    percentage_complete = Column(Float, default=0.0)
    
    # Tracking
    started_at = Column(DateTime, default=datetime.utcnow)
    last_progress_at = Column(DateTime, default=datetime.utcnow)
    
    # Details
    progress_breakdown = Column(JSON, nullable=True)  # {"videos_watched": 10, "quizzes_taken": 5}
    
    # Status
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
