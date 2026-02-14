"""Learning paths and modules models."""

from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Float, Boolean, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, date
from database.core.base import BaseModel
from database.core.enums import ModuleStatus


class LearningPath(BaseModel):
    """Personalized learning paths for users."""
    __tablename__ = "learning_paths"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Path identification
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    target_career = Column(String(200), nullable=True)
    target_job_role = Column(String(200), nullable=True)
    
    # Progress
    total_modules = Column(Integer, default=0)
    completed_modules = Column(Integer, default=0)
    in_progress_modules = Column(Integer, default=0)
    completion_percentage = Column(Float, default=0.0)
    
    # Timeline
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    target_completion_date = Column(Date, nullable=True)
    estimated_completion_date = Column(Date, nullable=True)
    actual_completion_date = Column(DateTime, nullable=True)
    
    # Adaptivity
    adaptivity_score = Column(Float, default=0.0)  # How much path has adapted
    adaptation_count = Column(Integer, default=0)  # Number of times adapted
    last_adapted_at = Column(DateTime, nullable=True)
    
    # Status
    status = Column(String(50), default="draft")  # draft, active, completed, archived
    is_active = Column(Boolean, default=True)
    is_personalized = Column(Boolean, default=True)
    
    # AI recommendations
    ai_confidence_score = Column(Float, nullable=True)
    recommended_because = Column(JSON, nullable=True)  # ["skill_gap", "career_goal"]
    
    # Relationships
    user = relationship("User", back_populates="learning_paths")
    modules = relationship("PathModule", back_populates="learning_path", order_by="PathModule.module_order", cascade="all, delete-orphan")
    sessions = relationship("LearningSession", back_populates="learning_path")


class PathModule(BaseModel):
    """Individual modules within a learning path."""
    __tablename__ = "path_modules"
    
    path_id = Column(Integer, ForeignKey("learning_paths.id"), nullable=False)
    
    # Ordering
    module_order = Column(Integer, nullable=False)
    
    # Content reference
    content_id = Column(Integer, nullable=False)  # Reference to content table
    content_type = Column(String(50), nullable=False)  # course, lesson, quiz, project
    
    # Module info
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    estimated_duration_minutes = Column(Integer, nullable=True)
    
    # Status
    status = Column(Enum(ModuleStatus), default=ModuleStatus.LOCKED)
    completion_percentage = Column(Float, default=0.0)
    
    # Progress
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    time_spent_minutes = Column(Integer, default=0)
    
    # Dependencies
    prerequisites = Column(JSON, nullable=True)  # [module_id, module_id]
    unlocks_modules = Column(JSON, nullable=True)  # [module_id]
    
    # AI adaptivity
    difficulty_adjusted = Column(Boolean, default=False)
    original_difficulty = Column(String(50), nullable=True)
    adjusted_difficulty = Column(String(50), nullable=True)
    ai_recommended = Column(Boolean, default=False)
    recommendation_reason = Column(String(255), nullable=True)
    
    # Scoring
    module_score = Column(Float, nullable=True)  # From assessments
    max_possible_score = Column(Float, nullable=True)
    
    # Relationships
    learning_path = relationship("LearningPath", back_populates="modules")
    sessions = relationship("LearningSession", back_populates="module")


class PathAdaptation(BaseModel):
    """Track how learning paths are adapted by AI."""
    __tablename__ = "path_adaptations"
    
    path_id = Column(Integer, ForeignKey("learning_paths.id"), nullable=False)
    
    # Change details
    adaptation_type = Column(String(100), nullable=False)  # difficulty_adjustment, content_swap, reorder
    change_description = Column(Text, nullable=True)
    
    # Before/After
    previous_state = Column(JSON, nullable=False)
    new_state = Column(JSON, nullable=False)
    
    # Reasoning
    trigger_event = Column(String(255), nullable=True)  # Why adaptation happened
    user_performance_data = Column(JSON, nullable=True)
    ai_confidence = Column(Float, nullable=True)
    
    # User feedback
    user_accepted = Column(Boolean, default=True)
    user_feedback = Column(Text, nullable=True)
    
    adapted_at = Column(DateTime, default=datetime.utcnow)


class PathTemplate(BaseModel):
    """Reusable learning path templates."""
    __tablename__ = "path_templates"
    
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    
    # Target
    target_career = Column(String(200), nullable=True)
    target_job_role = Column(String(200), nullable=True)
    required_nsqf_level = Column(Integer, nullable=True)
    
    # Content
    default_modules = Column(JSON, nullable=False)  # Ordered list of content
    estimated_duration_hours = Column(Integer, nullable=True)
    
    # Skills covered
    skills_targeted = Column(JSON, nullable=True)  # [skill_id, skill_id]
    prerequisites = Column(JSON, nullable=True)  # Required before starting
    
    # Metadata
    category = Column(String(100), nullable=True)
    difficulty_level = Column(String(50), default="mixed")
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    
    usage_count = Column(Integer, default=0)
    average_completion_rate = Column(Float, nullable=True)
