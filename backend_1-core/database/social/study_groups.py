"""Study groups models."""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database.core.base import BaseModel


class StudyGroup(BaseModel):
    """Study group definitions."""
    __tablename__ = "study_groups"
    
    # Basic info
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    avatar_url = Column(String(500), nullable=True)
    
    # Settings
    max_members = Column(Integer, default=10)
    is_private = Column(Boolean, default=False)
    invite_code = Column(String(20), nullable=True, unique=True)
    
    # Focus
    topic = Column(String(200), nullable=True)
    skill_focus = Column(JSON, nullable=True)  # [skill_id, skill_id]
    course_focus = Column(JSON, nullable=True)  # [course_id]
    
    # Stats
    current_members = Column(Integer, default=1)
    total_sessions = Column(Integer, default=0)
    total_xp_earned = Column(Integer, default=0)
    
    # Schedule
    meeting_schedule = Column(JSON, nullable=True)  # {"monday": "18:00", "wednesday": "18:00"}
    next_meeting_at = Column(DateTime, nullable=True)
    
    # Creator
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    members = relationship("GroupMember", back_populates="group", cascade="all, delete-orphan")
    sessions = relationship("GroupStudySession", back_populates="group", cascade="all, delete-orphan")
    creator = relationship("User", foreign_keys=[created_by])


class GroupMember(BaseModel):
    """Membership in study groups."""
    __tablename__ = "group_members"
    
    group_id = Column(Integer, ForeignKey("study_groups.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Role
    role = Column(String(50), default="member")  # admin, moderator, member
    
    # Membership details
    joined_at = Column(DateTime, default=datetime.utcnow)
    invited_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Stats
    xp_contributed = Column(Integer, default=0)
    sessions_attended = Column(Integer, default=0)
    streak_days = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True)
    left_at = Column(DateTime, nullable=True)
    
    # Preferences
    notifications_enabled = Column(Boolean, default=True)
    
    # Relationships
    group = relationship("StudyGroup", back_populates="members")
    user = relationship("User", back_populates="group_memberships")
    inviter = relationship("User", foreign_keys=[invited_by])


class GroupStudySession(BaseModel):
    """Study sessions conducted by groups."""
    __tablename__ = "group_study_sessions"
    
    group_id = Column(Integer, ForeignKey("study_groups.id"), nullable=False)
    
    # Session details
    title = Column(String(200), nullable=True)
    description = Column(Text, nullable=True)
    topic = Column(String(200), nullable=True)
    
    # Timing
    scheduled_at = Column(DateTime, nullable=False)
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    
    # Status
    status = Column(String(50), default="scheduled")  # scheduled, active, completed, cancelled
    
    # Participants
    max_participants = Column(Integer, nullable=True)
    actual_participants = Column(Integer, default=0)
    
    # Content
    agenda = Column(JSON, nullable=True)
    resources_shared = Column(JSON, nullable=True)
    
    # Results
    total_xp_earned = Column(Integer, default=0)
    notes = Column(Text, nullable=True)
    
    # Relationships
    group = relationship("StudyGroup", back_populates="sessions")
    participants = relationship("GroupSessionParticipant", back_populates="session", cascade="all, delete-orphan")


class GroupSessionParticipant(BaseModel):
    """Individual participation in group sessions."""
    __tablename__ = "group_session_participants"
    
    session_id = Column(Integer, ForeignKey("group_study_sessions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Attendance
    joined_at = Column(DateTime, nullable=True)
    left_at = Column(DateTime, nullable=True)
    duration_minutes = Column(Integer, default=0)
    
    # Engagement
    messages_sent = Column(Integer, default=0)
    questions_asked = Column(Integer, default=0)
    resources_shared = Column(Integer, default=0)
    
    # Rewards
    xp_earned = Column(Integer, default=0)
    attendance_streak = Column(Integer, default=0)
    
    # Feedback
    rating = Column(Integer, nullable=True)  # 1-5
    feedback = Column(Text, nullable=True)
    
    # Relationships
    session = relationship("GroupStudySession", back_populates="participants")
    user = relationship("User")
