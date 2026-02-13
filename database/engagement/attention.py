"""Attention span and focus tracking models."""

from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey, Interval
from sqlalchemy.orm import relationship
from datetime import datetime
from database.core.base import BaseModel


class AttentionSpan(BaseModel):
    """Track micro-moments of attention during learning sessions."""
    __tablename__ = "attention_spans"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    session_id = Column(Integer, ForeignKey("learning_sessions.id"), nullable=False, index=True)
    
    # Focus period timing
    focus_start_time = Column(DateTime, default=datetime.utcnow)
    focus_end_time = Column(DateTime, nullable=True)
    duration_seconds = Column(Integer, default=0)
    
    # Content context
    content_id = Column(String(100), nullable=True)
    content_type = Column(String(50), nullable=True)  # video, text, quiz
    
    # Distraction tracking
    tab_switches = Column(Integer, default=0)
    window_blur_count = Column(Integer, default=0)  # Lost focus from window
    idle_time_seconds = Column(Integer, default=0)
    pause_count = Column(Integer, default=0)
    resume_count = Column(Integer, default=0)
    
    # Scores
    attention_score = Column(Float, nullable=True)  # 0-100 calculated
    focus_quality = Column(String(20), nullable=True)  # high, medium, low
    
    # Content progress during this span
    content_position_start = Column(Float, nullable=True)  # % or timestamp
    content_position_end = Column(Float, nullable=True)
    
    # Relationships
    user = relationship("User")
    session = relationship("LearningSession", back_populates="attention_spans")


class DistractionEvent(BaseModel):
    """Track specific distraction events."""
    __tablename__ = "distraction_events"
    
    attention_span_id = Column(Integer, ForeignKey("attention_spans.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(Integer, ForeignKey("learning_sessions.id"), nullable=False)
    
    # Event details
    event_type = Column(String(50), nullable=False)  # tab_switch, notification, idle_timeout
    occurred_at = Column(DateTime, default=datetime.utcnow)
    
    # Context
    from_url = Column(String(500), nullable=True)  # Where they went
    duration_seconds = Column(Integer, nullable=True)  # How long distracted
    
    # Recovery
    returned_at = Column(DateTime, nullable=True)
    return_method = Column(String(50), nullable=True)  # click, auto_redirect


class FocusPattern(BaseModel):
    """Aggregated focus patterns per user (ML-derived)."""
    __tablename__ = "focus_patterns"
    
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Optimal conditions
    optimal_session_length = Column(Integer, nullable=True)  # minutes
    optimal_break_interval = Column(Integer, nullable=True)  # minutes
    optimal_time_of_day = Column(String(20), nullable=True)
    
    # Focus metrics
    avg_attention_score = Column(Float, default=0.0)
    peak_attention_time = Column(String(20), nullable=True)
    attention_decay_rate = Column(Float, nullable=True)  # % per minute
    
    # Distraction triggers
    common_distractions = Column(JSON, nullable=True)  # ["notifications", "social_media"]
    attention_recovery_time = Column(Float, nullable=True)  # avg seconds to refocus
    
    # Recommendations
    recommended_pomodoro_length = Column(Integer, default=25)  # minutes
    recommended_break_duration = Column(Integer, default=5)  # minutes
    
    # ML metadata
    model_version = Column(String(20), nullable=True)
    last_analyzed = Column(DateTime, nullable=True)
    confidence_score = Column(Float, default=0.0)
