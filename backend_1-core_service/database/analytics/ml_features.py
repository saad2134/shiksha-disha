"""ML features and model tracking."""

from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database.core.base import BaseModel


class MLFeatureStore(BaseModel):
    """Cached ML features for users."""
    __tablename__ = "ml_feature_store"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    feature_version = Column(String(20), nullable=False)
    
    # User features
    engagement_features = Column(JSON, nullable=True)
    behavior_features = Column(JSON, nullable=True)
    content_features = Column(JSON, nullable=True)
    social_features = Column(JSON, nullable=True)
    
    # Derived features
    churn_prediction = Column(Float, nullable=True)
    ltv_prediction = Column(Float, nullable=True)
    next_best_action = Column(String(100), nullable=True)
    recommended_difficulty = Column(String(50), nullable=True)
    
    # Computed
    computed_at = Column(DateTime, default=datetime.utcnow)
    feature_hash = Column(String(64), nullable=True)  # For cache validation


class MLModelVersion(BaseModel):
    """ML model version tracking."""
    __tablename__ = "ml_model_versions"
    
    # Model info
    model_name = Column(String(100), nullable=False)
    model_version = Column(String(20), nullable=False)
    model_type = Column(String(50), nullable=False)  # churn_prediction, recommendation, etc.
    
    # Storage
    model_path = Column(String(500), nullable=False)
    artifact_hash = Column(String(64), nullable=True)
    
    # Training info
    training_data_start = Column(DateTime, nullable=True)
    training_data_end = Column(DateTime, nullable=True)
    training_samples = Column(Integer, nullable=True)
    training_duration_seconds = Column(Integer, nullable=True)
    
    # Performance
    training_metrics = Column(JSON, nullable=True)  # {"accuracy": 0.95, "f1": 0.92}
    validation_metrics = Column(JSON, nullable=True)
    test_metrics = Column(JSON, nullable=True)
    
    # Deployment
    is_deployed = Column(Boolean, default=False)
    deployed_at = Column(DateTime, nullable=True)
    deployment_status = Column(String(50), default="staging")  # staging, production, archived
    
    # A/B testing
    traffic_percentage = Column(Float, default=0.0)
    
    # Metadata
    created_by = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)


class MLPredictionLog(BaseModel):
    """Log of ML predictions for auditing and analysis."""
    __tablename__ = "ml_prediction_logs"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    model_version_id = Column(Integer, ForeignKey("ml_model_versions.id"), nullable=False)
    
    # Prediction details
    prediction_type = Column(String(50), nullable=False)
    input_features = Column(JSON, nullable=True)
    prediction_value = Column(JSON, nullable=False)  # Can be single value or complex object
    confidence_score = Column(Float, nullable=True)
    
    # Context
    context = Column(JSON, nullable=True)  # Page, time of day, etc.
    
    # Outcome (updated later)
    actual_outcome = Column(JSON, nullable=True)  # What actually happened
    accuracy = Column(Float, nullable=True)  # Was the prediction correct?
    
    # Timestamp
    predicted_at = Column(DateTime, default=datetime.utcnow)
    outcome_recorded_at = Column(DateTime, nullable=True)


class RecommendationLog(BaseModel):
    """Log of content recommendations."""
    __tablename__ = "recommendation_logs"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Recommendation details
    recommendation_type = Column(String(50), nullable=False)  # course, path, content
    recommended_items = Column(JSON, nullable=False)  # [{item_id, score, reason}]
    
    # Context
    context_type = Column(String(50), nullable=True)  # homepage, completion, search
    context_data = Column(JSON, nullable=True)
    
    # Algorithm info
    algorithm_version = Column(String(20), nullable=True)
    diversification_applied = Column(Boolean, default=False)
    
    # User interaction
    clicked_items = Column(JSON, nullable=True)  # Which recommendations were clicked
    converted = Column(Boolean, default=False)
    
    # Metrics
    click_through_rate = Column(Float, nullable=True)
    conversion_rate = Column(Float, nullable=True)
    
    recommended_at = Column(DateTime, default=datetime.utcnow)
