"""Daily login tracking models."""

from sqlalchemy import Column, Integer, String, Date, DateTime, Float, Boolean, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime, date
from database.core.base import BaseModel


class DailyLogin(BaseModel):
    """Track daily user logins for streaks and engagement analytics."""
    __tablename__ = "daily_logins"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    login_date = Column(Date, nullable=False, index=True)
    
    # Login details
    first_login_at = Column(DateTime, default=datetime.utcnow)
    last_activity_at = Column(DateTime, nullable=True)
    logout_time = Column(DateTime, nullable=True)
    
    # Session metrics
    session_count = Column(Integer, default=1)
    total_time_minutes = Column(Integer, default=0)
    
    # Device info
    device_type = Column(String(50))  # mobile, desktop, tablet
    platform = Column(String(50))
    
    # Streak tracking
    consecutive_days = Column(Integer, default=0)
    is_first_login_of_day = Column(Boolean, default=True)
    streak_continued = Column(Boolean, default=True)
    
    # Engagement metrics
    content_items_consumed = Column(Integer, default=0)
    quizzes_completed = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="daily_logins")
    
    # Composite index for efficient queries
    __table_args__ = (
        Index('idx_user_date', 'user_id', 'login_date', unique=True),
    )


class LearningSession(BaseModel):
    """Track individual learning sessions."""
    __tablename__ = "learning_sessions"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Session timing
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    duration_seconds = Column(Integer, default=0)
    
    # Content context
    content_id = Column(String(100), nullable=True, index=True)
    content_type = Column(String(50), nullable=True)  # video, text, quiz
    module_id = Column(Integer, ForeignKey("path_modules.id"), nullable=True)
    path_id = Column(Integer, ForeignKey("learning_paths.id"), nullable=True)
    
    # Engagement metrics
    engagement_score = Column(Float, nullable=True)  # 0-100
    dropout_risk = Column(Float, nullable=True)  # 0-1 probability
    completion_percentage = Column(Float, default=0.0)
    
    # Session quality
    was_interrupted = Column(Boolean, default=False)
    interruption_count = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    events = relationship("BehaviorEvent", back_populates="session", cascade="all, delete-orphan")
    attention_spans = relationship("AttentionSpan", back_populates="session", cascade="all, delete-orphan")


class BehaviorEvent(BaseModel):
    """Track granular user behavior events."""
    __tablename__ = "behavior_events"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    session_id = Column(Integer, ForeignKey("learning_sessions.id"), nullable=True, index=True)
    
    # Event details
    event_type = Column(String(50), nullable=False, index=True)  # video_play, video_pause, scroll, click
    event_subtype = Column(String(50), nullable=True)
    
    # Content context
    content_id = Column(String(100), nullable=True)
    content_type = Column(String(50), nullable=True)
    
    # Event data
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    metadata = Column(JSON, nullable=True)  # {playback_speed, scroll_depth, etc.}
    
    # Relationships
    user = relationship("User", back_populates="behavior_events")
    session = relationship("LearningSession", back_populates="events")
    
    # Indexes for analytics queries
    __table_args__ = (
        Index('idx_user_event_time', 'user_id', 'event_type', 'timestamp'),
    )


class UserEngagementProfile(BaseModel):
    """Aggregated engagement metrics per user."""
    __tablename__ = "user_engagement_profiles"
    
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Overall engagement
    avg_engagement_score = Column(Float, default=0.0)  # 0-100
    total_sessions = Column(Integer, default=0)
    total_learning_time_minutes = Column(Integer, default=0)
    
    # Content preferences (detected from behavior)
    preferred_content_type = Column(String(50), nullable=True)
    preferred_difficulty = Column(String(50), nullable=True)
    preferred_session_duration = Column(Integer, nullable=True)  # minutes
    optimal_time_of_day = Column(String(20), nullable=True)  # morning, afternoon, evening
    
    # Risk assessment
    dropout_risk_score = Column(Float, default=0.0)  # 0-1 probability
    churn_probability = Column(Float, default=0.0)
    
    # Activity patterns
    avg_sessions_per_week = Column(Float, default=0.0)
    avg_time_per_session = Column(Float, default=0.0)  # minutes
    last_active_date = Column(Date, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="engagement_profile")
