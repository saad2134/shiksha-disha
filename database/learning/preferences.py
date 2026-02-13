"""Learning preferences and personalization models."""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database.core.base import BaseModel
from database.core.enums import LearningStyle


class LearningPreference(BaseModel):
    """User's learning preferences and style."""
    __tablename__ = "learning_preferences"
    
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # VARK Model scores (should sum to 1.0)
    visual_score = Column(Float, default=0.25)
    auditory_score = Column(Float, default=0.25)
    reading_score = Column(Float, default=0.25)
    kinesthetic_score = Column(Float, default=0.25)
    
    # Detected dominant style
    dominant_style = Column(String(50), default="multimodal")  # visual, auditory, reading, kinesthetic, multimodal
    style_confidence = Column(Float, default=0.5)
    
    # Temporal preferences
    preferred_time_slots = Column(JSON, default=["evening"])  # ["morning", "afternoon", "evening", "night"]
    optimal_session_duration = Column(Integer, default=30)  # minutes
    optimal_break_interval = Column(Integer, default=10)  # minutes
    
    # Content preferences
    preferred_pace = Column(String(50), default="moderate")  # slow, moderate, fast
    liked_content_types = Column(JSON, default=[])  # ["video", "interactive"]
    disliked_content_types = Column(JSON, default=[])
    
    # Format preferences
    prefers_subtitles = Column(Boolean, default=True)
    prefers_transcripts = Column(Boolean, default=False)
    prefers_audio_only = Column(Boolean, default=False)
    prefers_text_summary = Column(Boolean, default=True)
    
    # Gamification preferences
    gamification_enabled = Column(Boolean, default=True)
    likes_competition = Column(Boolean, default=True)
    likes_collaboration = Column(Boolean, default=True)
    notification_frequency = Column(String(50), default="moderate")  # minimal, moderate, frequent
    
    # Accessibility
    high_contrast_mode = Column(Boolean, default=False)
    large_text = Column(Boolean, default=False)
    reduced_motion = Column(Boolean, default=False)
    screen_reader_optimized = Column(Boolean, default=False)
    
    # AI-detected metadata
    detected_learning_style = Column(String(50), nullable=True)
    detection_confidence_score = Column(Float, default=0.0)
    behavior_based_scores = Column(JSON, nullable=True)
    last_analyzed_at = Column(DateTime, nullable=True)
    
    # User-set overrides
    user_overrides = Column(JSON, nullable=True)  # Fields user has manually set
    
    # Relationships
    user = relationship("User", back_populates="learning_preferences")


class ContentPreference(BaseModel):
    """Content-specific preferences."""
    __tablename__ = "content_preferences"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content_type = Column(String(50), nullable=False)  # video, text, quiz, etc.
    
    # Preference scores (-1 to 1, where -1 = dislike, 1 = love)
    preference_score = Column(Float, default=0.0)
    
    # Engagement metrics
    times_consumed = Column(Integer, default=0)
    avg_engagement_score = Column(Float, default=0.0)
    completion_rate = Column(Float, default=0.0)
    
    # Feedback
    explicit_rating = Column(Integer, nullable=True)  # 1-5 stars
    feedback_notes = Column(Text, nullable=True)
    
    # AI recommendations
    ai_recommendation_score = Column(Float, default=0.0)
    recommended_frequency = Column(String(50), default="normal")  # more, normal, less
    
    last_updated = Column(DateTime, default=datetime.utcnow)


class LearningContextPreference(BaseModel):
    """Preferences for specific learning contexts."""
    __tablename__ = "learning_context_preferences"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Context
    context_type = Column(String(100), nullable=False)  # "morning_commute", "lunch_break", "evening_study"
    day_of_week = Column(Integer, nullable=True)  # 0-6, NULL = any day
    
    # Preferences for this context
    preferred_content_type = Column(String(50), nullable=True)
    preferred_duration_minutes = Column(Integer, nullable=True)
    preferred_difficulty = Column(String(50), nullable=True)
    notification_enabled = Column(Boolean, default=True)
    
    # Performance in this context
    avg_attention_score = Column(Float, nullable=True)
    completion_rate = Column(Float, nullable=True)
    
    is_active = Column(Boolean, default=True)


class DifficultyCalibration(BaseModel):
    """Per-user difficulty calibration."""
    __tablename__ = "difficulty_calibrations"
    
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Calibration factors
    difficulty_modifier = Column(Float, default=0.0)  # -0.5 to +0.5, applied to all content
    
    # Category-specific calibrations
    calibration_by_category = Column(JSON, default={})  # {"math": -0.2, "language": 0.1}
    
    # Performance history
    accuracy_by_difficulty = Column(JSON, default={})  # {"easy": 0.95, "medium": 0.75, "hard": 0.45}
    
    # Auto-adjustment settings
    auto_adjust_enabled = Column(Boolean, default=True)
    last_adjusted_at = Column(DateTime, nullable=True)
    adjustment_history = Column(JSON, default=[])
