"""Streak system models."""

from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey, Text, Index
from sqlalchemy.orm import relationship
from datetime import datetime, date
from database.core.base import BaseModel


class UserStreak(BaseModel):
    """Track user streak information."""
    __tablename__ = "user_streaks"
    
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Streak counts
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    total_active_days = Column(Integer, default=0)
    
    # Streak timing
    streak_start_date = Column(Date, nullable=True)
    last_activity_date = Column(Date, nullable=True)
    
    # Freeze system
    freeze_count = Column(Integer, default=0)
    max_freezes = Column(Integer, default=3)  # Per month or total
    freezes_used_this_month = Column(Integer, default=0)
    
    # Streak protection
    has_streak_protector = Column(Boolean, default=False)
    protector_expires_at = Column(DateTime, nullable=True)
    
    # Milestone tracking
    next_milestone = Column(Integer, default=7)  # Next milestone day
    milestones_achieved = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="streak")
    activities = relationship("StreakActivity", back_populates="user_streak", cascade="all, delete-orphan")
    freezes = relationship("StreakFreeze", back_populates="user_streak", cascade="all, delete-orphan")


class StreakActivity(BaseModel):
    """Daily streak activity log."""
    __tablename__ = "streak_activities"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_streak_id = Column(Integer, ForeignKey("user_streaks.id"), nullable=False)
    
    # Activity date
    activity_date = Column(Date, nullable=False, index=True)
    
    # Activity metrics
    minutes_active = Column(Integer, default=0)
    sessions_completed = Column(Integer, default=0)
    modules_completed = Column(Integer, default=0)
    
    # Content breakdown
    content_type = Column(String(50), nullable=True)  # Primary content type
    content_types_consumed = Column(JSON, nullable=True)  # ["video", "quiz"]
    
    # Streak status
    streak_continued = Column(Boolean, default=True)
    streak_day_number = Column(Integer, nullable=True)  # Which day of the streak
    
    # Points earned
    points_earned = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="streak_activities")
    user_streak = relationship("UserStreak", back_populates="activities")
    
    __table_args__ = (
        Index('idx_user_activity_date', 'user_id', 'activity_date', unique=True),
    )


class StreakFreeze(BaseModel):
    """Streak freeze (vacation mode) records."""
    __tablename__ = "streak_freezes"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_streak_id = Column(Integer, ForeignKey("user_streaks.id"), nullable=False)
    
    # Freeze details
    freeze_date = Column(Date, nullable=False)
    reason = Column(String(100), nullable=True)  # vacation, sick, emergency
    
    # Status
    is_used = Column(Boolean, default=False)
    used_at = Column(DateTime, nullable=True)
    
    # Request info
    requested_at = Column(DateTime, default=datetime.utcnow)
    approved = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User")
    user_streak = relationship("UserStreak", back_populates="freezes")


class StreakMilestone(BaseModel):
    """Streak milestone achievements."""
    __tablename__ = "streak_milestones"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Milestone details
    milestone_days = Column(Integer, nullable=False)  # 7, 30, 60, 100, 365
    milestone_type = Column(String(50), default="daily_streak")  # daily, weekly, perfect_week
    
    # Achievement info
    achieved_at = Column(DateTime, default=datetime.utcnow)
    
    # Rewards
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=True)
    points_awarded = Column(Integer, default=0)
    reward_claimed = Column(Boolean, default=False)
    claimed_at = Column(DateTime, nullable=True)
    
    # Bonus rewards
    bonus_unlocked = Column(JSON, nullable=True)  # {theme: "gold", feature: "priority_support"}
    
    # Relationships
    user = relationship("User")
    badge = relationship("Badge")
