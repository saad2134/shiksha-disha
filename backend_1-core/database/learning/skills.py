"""Skills and mastery tracking models."""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, date
from database.core.base import BaseModel


class Skill(BaseModel):
    """Skill definitions aligned with NSQF."""
    __tablename__ = "skills"
    
    # Basic info
    name = Column(String(200), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    short_description = Column(String(500), nullable=True)
    
    # NSQF alignment
    nsqf_level = Column(Integer, nullable=True)  # 1-10
    nsqf_sector = Column(String(100), nullable=True)
    nsqf_job_role = Column(String(200), nullable=True)
    
    # Hierarchy
    parent_skill_id = Column(Integer, ForeignKey("skills.id"), nullable=True)
    skill_level = Column(Integer, default=1)  # 1 = basic, higher = advanced
    
    # Relationships
    sub_skills = relationship("Skill", backref="parent_skill", remote_side="Skill.id")
    prerequisites = Column(JSON, nullable=True)  # [skill_id, skill_id]
    
    # Metadata
    category = Column(String(100), nullable=True)
    tags = Column(JSON, nullable=True)
    estimated_hours_to_learn = Column(Integer, nullable=True)
    
    # Mastery tracking
    mastery_definitions = Column(JSON, nullable=True)  # {"beginner": 0-40, "intermediate": 41-70}
    
    # Relationships
    user_mastery = relationship("SkillMastery", back_populates="skill", cascade="all, delete-orphan")


class SkillMastery(BaseModel):
    """User's mastery level for each skill."""
    __tablename__ = "skill_mastery"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    
    # Mastery metrics
    mastery_level = Column(Float, default=0.0)  # 0-100
    proficiency_score = Column(Float, default=0.0)  # Calculated from assessments
    confidence_interval = Column(Float, nullable=True)  # ML uncertainty
    
    # Progress
    attempts_count = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)
    time_spent_minutes = Column(Integer, default=0)
    modules_completed = Column(Integer, default=0)
    assessments_passed = Column(Integer, default=0)
    
    # Current status
    current_level = Column(String(50), default="uninitiated")  # uninitiated, beginner, intermediate, advanced, expert
    is_certified = Column(Boolean, default=False)
    certification_date = Column(DateTime, nullable=True)
    
    # Spaced repetition for review
    next_review_date = Column(Date, nullable=True)
    review_interval_days = Column(Integer, default=1)
    ease_factor = Column(Float, default=2.5)
    last_reviewed = Column(DateTime, nullable=True)
    
    # Activity tracking
    last_practiced = Column(DateTime, nullable=True)
    streak_days = Column(Integer, default=0)  # Consecutive days practiced
    
    # Metadata
    weak_areas = Column(JSON, nullable=True)  # ["subskill1", "subskill2"]
    strong_areas = Column(JSON, nullable=True)
    recommended_focus = Column(JSON, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="skill_mastery")
    skill = relationship("Skill", back_populates="user_mastery")


class SkillAssessment(BaseModel):
    """Skill assessment definitions."""
    __tablename__ = "skill_assessments"
    
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    assessment_type = Column(String(50), default="adaptive")  # adaptive, fixed, project
    
    # Configuration
    difficulty_level = Column(String(50), default="adaptive")
    estimated_duration_minutes = Column(Integer, nullable=True)
    passing_score = Column(Float, default=70.0)
    max_score = Column(Float, default=100.0)
    
    # Content
    questions = Column(JSON, nullable=True)  # Question bank
    rubric = Column(JSON, nullable=True)  # For project-based
    
    # Mastery mapping
    mastery_thresholds = Column(JSON, nullable=True)  # {"beginner": 40, "intermediate": 65}
    
    is_active = Column(Boolean, default=True)
    version = Column(Integer, default=1)
