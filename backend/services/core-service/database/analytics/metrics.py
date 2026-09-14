"""Analytics and metrics models."""

from sqlalchemy import Column, Integer, String, Date, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, date
from database.core.base import BaseModel


class DailyMetrics(BaseModel):
    """Daily aggregated metrics."""
    __tablename__ = "daily_metrics"
    
    metric_date = Column(Date, nullable=False, index=True, unique=True)
    
    # User metrics
    total_users = Column(Integer, default=0)
    new_users = Column(Integer, default=0)
    active_users = Column(Integer, default=0)  # DAU
    returning_users = Column(Integer, default=0)
    
    # Engagement metrics
    total_sessions = Column(Integer, default=0)
    avg_session_duration = Column(Float, default=0.0)  # minutes
    total_learning_minutes = Column(Integer, default=0)
    
    # Content metrics
    content_views = Column(Integer, default=0)
    content_completions = Column(Integer, default=0)
    quiz_attempts = Column(Integer, default=0)
    quiz_completions = Column(Integer, default=0)
    
    # Gamification metrics
    streaks_started = Column(Integer, default=0)
    streaks_broken = Column(Integer, default=0)
    badges_earned = Column(Integer, default=0)
    duels_completed = Column(Integer, default=0)
    
    # Conversion metrics
    free_to_paid = Column(Integer, default=0)
    upgrades = Column(Integer, default=0)
    
    # Performance
    avg_load_time_ms = Column(Float, nullable=True)
    error_count = Column(Integer, default=0)
    
    # Custom metrics
    custom_metrics = Column(JSON, nullable=True)


class UserAnalytics(BaseModel):
    """Per-user analytics summary."""
    __tablename__ = "user_analytics"
    
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Activity summary
    first_seen_at = Column(DateTime, nullable=True)
    last_seen_at = Column(DateTime, nullable=True)
    total_sessions = Column(Integer, default=0)
    total_learning_minutes = Column(Integer, default=0)
    
    # Engagement cohort
    engagement_level = Column(String(50), default="new")  # new, casual, regular, power
    days_since_last_session = Column(Integer, nullable=True)
    
    # Retention
    day_1_retained = Column(Boolean, nullable=True)
    day_7_retained = Column(Boolean, nullable=True)
    day_30_retained = Column(Boolean, nullable=True)
    
    # Cohort
    cohort_date = Column(Date, nullable=True)  # First active date (week start)
    
    # Predictions
    churn_risk = Column(Float, default=0.0)
    predicted_ltv = Column(Float, nullable=True)
    
    # Feature usage
    features_used = Column(JSON, default=[])
    primary_feature = Column(String(100), nullable=True)
    
    # Updated
    last_calculated_at = Column(DateTime, default=datetime.utcnow)


class ContentAnalytics(BaseModel):
    """Per-content analytics."""
    __tablename__ = "content_analytics"
    
    content_id = Column(Integer, nullable=False, index=True)
    content_type = Column(String(50), nullable=False)
    
    # Views
    total_views = Column(Integer, default=0)
    unique_viewers = Column(Integer, default=0)
    
    # Engagement
    avg_engagement_score = Column(Float, default=0.0)
    avg_completion_rate = Column(Float, default=0.0)
    avg_time_spent_minutes = Column(Float, default=0.0)
    
    # Quality metrics
    drop_off_points = Column(JSON, nullable=True)  # [{timestamp: 120, percentage: 0.3}]
    replay_count = Column(Integer, default=0)
    
    # Feedback
    rating_avg = Column(Float, nullable=True)
    rating_count = Column(Integer, default=0)
    
    # Difficulty (for assessments)
    avg_score = Column(Float, nullable=True)
    pass_rate = Column(Float, nullable=True)
    
    # Updated
    last_calculated_at = Column(DateTime, default=datetime.utcnow)


class ABTest(BaseModel):
    """A/B test tracking."""
    __tablename__ = "ab_tests"
    
    # Test details
    test_name = Column(String(200), nullable=False)
    test_key = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    
    # Variants
    variant_a_name = Column(String(100), default="Control")
    variant_b_name = Column(String(100), default="Treatment")
    
    # Status
    status = Column(String(50), default="draft")  # draft, running, paused, completed
    
    # Timing
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)
    
    # Targeting
    target_percentage = Column(Float, default=50.0)  # % of users in test
    target_criteria = Column(JSON, nullable=True)  # {"platform": "mobile", "new_users_only": true}
    
    # Metrics
    primary_metric = Column(String(100), nullable=False)  # conversion_rate, engagement, etc.
    secondary_metrics = Column(JSON, nullable=True)
    
    # Results
    winner = Column(String(10), nullable=True)  # A, B, or NULL if tie
    confidence_level = Column(Float, nullable=True)
    uplift_percentage = Column(Float, nullable=True)


class ABTestAssignment(BaseModel):
    """User assignments to A/B test variants."""
    __tablename__ = "ab_test_assignments"
    
    test_id = Column(Integer, ForeignKey("ab_tests.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    variant = Column(String(10), nullable=False)  # A or B
    assigned_at = Column(DateTime, default=datetime.utcnow)
    
    # Results
    converted = Column(Boolean, default=False)
    converted_at = Column(DateTime, nullable=True)
    
    # Metrics
    primary_metric_value = Column(Float, nullable=True)
    secondary_metrics = Column(JSON, nullable=True)
