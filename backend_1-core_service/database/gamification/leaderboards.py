"""Leaderboard models."""

from sqlalchemy import Column, Integer, String, Date, DateTime, Float, Boolean, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime, date
from database.core.base import BaseModel


class Leaderboard(BaseModel):
    """Leaderboard definitions."""
    __tablename__ = "leaderboards"
    
    # Identification
    category = Column(String(50), nullable=False)  # weekly_streak, monthly_xp, all_time
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    
    # Scope
    region = Column(String(100), nullable=True)  # NULL = global
    course_id = Column(Integer, nullable=True)  # NULL = all courses
    skill_id = Column(Integer, nullable=True)  # NULL = all skills
    
    # Time period
    period_type = Column(String(20), nullable=False)  # weekly, monthly, all_time
    period_start = Column(Date, nullable=True)  # For time-bound leaderboards
    period_end = Column(Date, nullable=True)
    
    # Configuration
    max_entries = Column(Integer, default=100)
    is_active = Column(Boolean, default=True)
    is_public = Column(Boolean, default=True)
    
    # Metadata
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    entries = relationship("LeaderboardEntry", back_populates="leaderboard", cascade="all, delete-orphan")


class LeaderboardEntry(BaseModel):
    """Individual leaderboard entries."""
    __tablename__ = "leaderboard_entries"
    
    leaderboard_id = Column(Integer, ForeignKey("leaderboards.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Ranking
    rank = Column(Integer, nullable=False, index=True)
    previous_rank = Column(Integer, nullable=True)
    rank_change = Column(Integer, default=0)  # +5 (up), -3 (down)
    
    # Score
    score = Column(Float, nullable=False)
    previous_score = Column(Float, nullable=True)
    
    # Details
    breakdown = Column(JSON, nullable=True)  # {"xp": 1000, "streak": 7, "quizzes": 5}
    
    # Comparison to neighbors
    gap_to_first = Column(Float, nullable=True)
    gap_to_next = Column(Float, nullable=True)
    
    # Rewards
    reward_claimed = Column(Boolean, default=False)
    reward_type = Column(String(50), nullable=True)  # badge, points, title
    reward_value = Column(Integer, nullable=True)
    
    # Timestamps
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    leaderboard = relationship("Leaderboard", back_populates="entries")
    user = relationship("User")
    
    __table_args__ = (
        Index('idx_leaderboard_user', 'leaderboard_id', 'user_id', unique=True),
        Index('idx_leaderboard_rank', 'leaderboard_id', 'rank'),
    )


class LeaderboardHistory(BaseModel):
    """Historical leaderboard data for analytics."""
    __tablename__ = "leaderboard_histories"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = Column(String(50), nullable=False)
    period_start = Column(Date, nullable=False)
    
    # Final results
    final_rank = Column(Integer, nullable=False)
    final_score = Column(Float, nullable=False)
    
    # Statistics
    percentile = Column(Float, nullable=True)  # Top 10%, etc.
    total_participants = Column(Integer, nullable=True)
    
    # Performance
    days_active = Column(Integer, nullable=True)
    average_daily_score = Column(Float, nullable=True)
    best_day_score = Column(Float, nullable=True)
    
    # Rewards received
    rewards_earned = Column(JSON, nullable=True)  # [{"type": "badge", "id": 123}]
