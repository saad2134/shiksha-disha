"""User management models."""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database.core.base import BaseModel


class User(BaseModel):
    """Core user model."""
    __tablename__ = "users"
    
    # Authentication
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=True)  # OAuth users may not have password
    
    # Profile info
    username = Column(String(50), unique=True, nullable=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    display_name = Column(String(100), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    
    # Preferences
    language = Column(String(10), default="en")
    timezone = Column(String(50), default="UTC")
    
    # Account status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    last_login_at = Column(DateTime, nullable=True)
    
    # Device tracking
    devices = relationship("UserDevice", back_populates="user", cascade="all, delete-orphan")
    
    # Engagement tracking
    daily_logins = relationship("DailyLogin", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("LearningSession", back_populates="user", cascade="all, delete-orphan")
    behavior_events = relationship("BehaviorEvent", back_populates="user", cascade="all, delete-orphan")
    
    # Gamification
    streak = relationship("UserStreak", back_populates="user", uselist=False, cascade="all, delete-orphan")
    points = relationship("UserPoints", back_populates="user", uselist=False, cascade="all, delete-orphan")
    badges = relationship("UserBadge", back_populates="user", cascade="all, delete-orphan")
    
    # Learning
    learning_preferences = relationship("LearningPreference", back_populates="user", uselist=False, cascade="all, delete-orphan")
    skill_mastery = relationship("SkillMastery", back_populates="user", cascade="all, delete-orphan")
    learning_paths = relationship("LearningPath", back_populates="user", cascade="all, delete-orphan")
    
    # Social
    connections_sent = relationship("UserConnection", foreign_keys="UserConnection.requester_id", back_populates="requester")
    connections_received = relationship("UserConnection", foreign_keys="UserConnection.addressee_id", back_populates="addressee")
    group_memberships = relationship("GroupMember", back_populates="user", cascade="all, delete-orphan")
    
    # Notifications
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    notification_preferences = relationship("NotificationPreference", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    @property
    def full_name(self):
        if self.first_name is not None and self.last_name is not None:
            return f"{self.first_name} {self.last_name}"
        return self.display_name or self.username or self.email


class UserDevice(BaseModel):
    """Track user devices for push notifications and analytics."""
    __tablename__ = "user_devices"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    device_type = Column(String(50))  # mobile, tablet, desktop
    platform = Column(String(50))  # ios, android, web
    push_token = Column(String(500), nullable=True)
    device_id = Column(String(255), nullable=True)  # Unique device identifier
    user_agent = Column(String(500), nullable=True)
    ip_address = Column(String(45), nullable=True)
    
    is_active = Column(Boolean, default=True)
    last_used_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="devices")
