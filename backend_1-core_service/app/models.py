from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    language = Column(String, default="en")
    hashed_password = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    actions = relationship("Action", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    devices = relationship("Device", back_populates="user")
    sessions = relationship("LearningSession", back_populates="user")
    behavior_events = relationship("BehaviorEvent", back_populates="user")
    engagement_profile = relationship("UserEngagementProfile", back_populates="user")
    streak = relationship("UserStreak", back_populates="user")
    streak_activities = relationship("StreakActivity", back_populates="user")

class Action(Base):
    __tablename__ = "actions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String, index=True)   # e.g. "skill_completed", "course_recommendation_clicked"
    payload = Column(JSON, nullable=True)  # arbitrary JSON describing action
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="actions")

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    meta = Column(JSON, nullable=True)
    delivered = Column(Boolean, default=False)
    read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")

class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    platform = Column(String, nullable=True)
    push_token = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="devices")


class LearningSession(Base):
    __tablename__ = "learning_sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content_id = Column(String, nullable=True)
    content_type = Column(String, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    duration_seconds = Column(Integer, default=0)
    engagement_score = Column(Integer, nullable=True)
    dropout_risk = Column(Float, nullable=True)
    
    user = relationship("User", back_populates="sessions")
    events = relationship("BehaviorEvent", back_populates="session")


class BehaviorEvent(Base):
    __tablename__ = "behavior_events"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(Integer, ForeignKey("learning_sessions.id"), nullable=True)
    event_type = Column(String, index=True)
    content_id = Column(String, nullable=True)
    content_type = Column(String, nullable=True)
    meta = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="behavior_events")
    session = relationship("LearningSession", back_populates="events")


class UserEngagementProfile(Base):
    __tablename__ = "user_engagement_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    avg_engagement_score = Column(Float, default=0.0)
    preferred_content_type = Column(String, nullable=True)
    preferred_difficulty = Column(String, nullable=True)
    dropout_risk_score = Column(Float, default=0.0)
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="engagement_profile")


class UserStreak(Base):
    __tablename__ = "user_streaks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_activity_date = Column(DateTime, nullable=True)
    streak_start_date = Column(DateTime, nullable=True)
    total_active_days = Column(Integer, default=0)
    freeze_count = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="streak")


class StreakActivity(Base):
    __tablename__ = "streak_activities"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_date = Column(DateTime, default=datetime.utcnow)
    minutes_active = Column(Integer, default=0)
    sessions_completed = Column(Integer, default=0)
    content_type = Column(String, nullable=True)
    streak_continued = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="streak_activities")
