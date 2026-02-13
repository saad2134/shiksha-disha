"""Notification system models."""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database.core.base import BaseModel
from database.core.enums import NotificationType


class Notification(BaseModel):
    """User notifications."""
    __tablename__ = "notifications"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Content
    type = Column(Enum(NotificationType), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    body = Column(Text, nullable=False)
    
    # Deep linking
    action_url = Column(String(500), nullable=True)  # Where to go when clicked
    action_type = Column(String(50), nullable=True)  # open_course, show_badge, start_quiz
    action_data = Column(JSON, nullable=True)  # {course_id: 123}
    
    # Media
    image_url = Column(String(500), nullable=True)
    icon = Column(String(100), nullable=True)  # Icon name or URL
    
    # Priority
    priority = Column(String(20), default="normal")  # low, normal, high, urgent
    
    # Delivery status
    is_delivered = Column(Boolean, default=False)
    delivered_at = Column(DateTime, nullable=True)
    delivery_method = Column(String(50), nullable=True)  # push, email, in_app
    
    # Read status
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime, nullable=True)
    
    # Interaction
    is_clicked = Column(Boolean, default=False)
    clicked_at = Column(DateTime, nullable=True)
    
    # Scheduling
    scheduled_for = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    
    # Grouping
    group_id = Column(String(100), nullable=True)  # For grouping similar notifications
    
    # Relationships
    user = relationship("User", back_populates="notifications")


class NotificationPreference(BaseModel):
    """User notification preferences."""
    __tablename__ = "notification_preferences"
    
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Channel preferences
    email_enabled = Column(Boolean, default=True)
    push_enabled = Column(Boolean, default=True)
    in_app_enabled = Column(Boolean, default=True)
    sms_enabled = Column(Boolean, default=False)
    
    # Category preferences
    streak_reminders = Column(Boolean, default=True)
    achievement_notifications = Column(Boolean, default=True)
    course_updates = Column(Boolean, default=True)
    social_notifications = Column(Boolean, default=True)
    marketing_notifications = Column(Boolean, default=False)
    
    # Timing
    quiet_hours_enabled = Column(Boolean, default=False)
    quiet_hours_start = Column(String(5), nullable=True)  # "22:00"
    quiet_hours_end = Column(String(5), nullable=True)  # "08:00"
    timezone = Column(String(50), default="UTC")
    
    # Frequency limits
    max_daily_notifications = Column(Integer, default=10)
    digest_mode = Column(Boolean, default=False)  # Group into daily digest
    digest_time = Column(String(5), default="09:00")
    
    # Relationships
    user = relationship("User", back_populates="notification_preferences")
    category_settings = relationship("NotificationCategorySetting", back_populates="preferences", cascade="all, delete-orphan")


class NotificationCategorySetting(BaseModel):
    """Detailed settings per notification category."""
    __tablename__ = "notification_category_settings"
    
    preference_id = Column(Integer, ForeignKey("notification_preferences.id"), nullable=False)
    category = Column(String(50), nullable=False)  # streak, achievement, social, etc.
    
    # Channel toggles
    email = Column(Boolean, default=True)
    push = Column(Boolean, default=True)
    in_app = Column(Boolean, default=True)
    sms = Column(Boolean, default=False)
    
    # Frequency
    frequency = Column(String(20), default="immediate")  # immediate, daily_digest, weekly_digest, off
    
    # Quiet hours override
    override_quiet_hours = Column(Boolean, default=False)
    
    # Relationships
    preferences = relationship("NotificationPreference", back_populates="category_settings")


class NotificationTemplate(BaseModel):
    """Templates for notifications."""
    __tablename__ = "notification_templates"
    
    # Identification
    template_key = Column(String(100), unique=True, nullable=False)
    type = Column(Enum(NotificationType), nullable=False)
    
    # Content (with placeholders)
    title_template = Column(String(200), nullable=False)  # "Streak in danger! {{hours_left}} hours left"
    body_template = Column(Text, nullable=False)
    
    # Localization
    language = Column(String(10), default="en")
    
    # Action
    action_type = Column(String(50), nullable=True)
    default_action_data = Column(JSON, nullable=True)
    
    # Settings
    default_priority = Column(String(20), default="normal")
    default_icon = Column(String(100), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    version = Column(Integer, default=1)
    
    # Analytics
    usage_count = Column(Integer, default=0)
    click_rate = Column(Float, nullable=True)
