"""Points and XP system models."""

from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey, JSON, Enum, Index
from sqlalchemy.orm import relationship
from datetime import datetime, date
from database.core.base import BaseModel
from database.core.enums import PointsActionType


class UserPoints(BaseModel):
    """User's points and level information."""
    __tablename__ = "user_points"
    
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Point totals
    total_points = Column(Integer, default=0)
    lifetime_points = Column(Integer, default=0)  # Never decreased
    redeemed_points = Column(Integer, default=0)
    
    # Level system
    current_level = Column(Integer, default=1)
    level_title = Column(String(50), default="Beginner")
    xp_to_next_level = Column(Integer, default=100)
    current_xp = Column(Integer, default=0)
    
    # Progress to next level
    level_progress_percentage = Column(Float, default=0.0)
    
    # Ranking
    global_rank = Column(Integer, nullable=True)
    regional_rank = Column(Integer, nullable=True)
    percentile = Column(Float, nullable=True)  # Top X%
    
    # Streaks
    daily_points_streak = Column(Integer, default=0)
    best_daily_points = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="points")
    transactions = relationship("PointsTransaction", back_populates="user_points", cascade="all, delete-orphan")


class PointsTransaction(BaseModel):
    """Individual point transactions."""
    __tablename__ = "points_transactions"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_points_id = Column(Integer, ForeignKey("user_points.id"), nullable=False)
    
    # Transaction details
    points = Column(Integer, nullable=False)  # +ve or -ve
    action_type = Column(Enum(PointsActionType), nullable=False)
    description = Column(String(255), nullable=False)
    
    # Context
    reference_id = Column(Integer, nullable=True)  # Course ID, Quiz ID, etc.
    reference_type = Column(String(50), nullable=True)  # course, quiz, badge
    
    # Metadata
    metadata = Column(JSON, nullable=True)  # {course_name: "Python Basics", streak_day: 5}
    
    # Multipliers
    base_points = Column(Integer, nullable=False)
    multiplier_applied = Column(Float, default=1.0)  # Streak bonus, etc.
    bonus_points = Column(Integer, default=0)
    
    # Status
    is_reverted = Column(Boolean, default=False)
    reverted_at = Column(DateTime, nullable=True)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship("User")
    user_points = relationship("UserPoints", back_populates="transactions")


class DailyPointsSummary(BaseModel):
    """Daily aggregation of points earned."""
    __tablename__ = "daily_points_summaries"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    summary_date = Column(Date, nullable=False)
    
    # Totals
    total_points = Column(Integer, default=0)
    transaction_count = Column(Integer, default=0)
    
    # Breakdown
    points_by_category = Column(JSON, default={})  # {"course_complete": 100, "streak": 50}
    
    # Streak info
    streak_day = Column(Integer, nullable=True)
    streak_multiplier = Column(Float, default=1.0)
    
    # Comparison
    vs_previous_day = Column(Integer, default=0)  # +10 or -5
    vs_average = Column(Float, default=0.0)  # Percentage
    
    __table_args__ = (
        Index('idx_user_date_summary', 'user_id', 'summary_date', unique=True),
    )


class LevelDefinition(BaseModel):
    """Level progression definitions."""
    __tablename__ = "level_definitions"
    
    level_number = Column(Integer, unique=True, nullable=False)
    title = Column(String(50), nullable=False)
    
    # Requirements
    xp_required = Column(Integer, nullable=False)
    cumulative_xp = Column(Integer, nullable=False)  # Total XP needed from level 1
    
    # Rewards
    reward_points = Column(Integer, default=0)
    reward_badge_id = Column(Integer, ForeignKey("badges.id"), nullable=True)
    reward_unlocks = Column(JSON, nullable=True)  # ["custom_theme", "analytics_dashboard"]
    
    # Visual
    icon_url = Column(String(500), nullable=True)
    color_scheme = Column(String(50), nullable=True)
