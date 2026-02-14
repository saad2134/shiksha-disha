"""Duel and challenge system models."""

from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey, JSON, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database.core.base import BaseModel
from database.core.enums import DuelStatus


class Duel(BaseModel):
    """Duel/challenge between users."""
    __tablename__ = "duels"
    
    # Participants
    challenger_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    opponent_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Challenge details
    challenge_type = Column(String(50), nullable=False)  # streak_battle, xp_race, quiz_race
    challenge_subtype = Column(String(50), nullable=True)  # specific rules
    
    # Description
    title = Column(String(200), nullable=True)
    description = Column(Text, nullable=True)
    rules = Column(JSON, nullable=True)  # {"goal": 100, "time_limit": 86400}
    
    # Stakes
    stakes_points = Column(Integer, default=0)
    stakes_badge_id = Column(Integer, nullable=True)
    
    # Status
    status = Column(Enum(DuelStatus), default=DuelStatus.PENDING)
    
    # Timing
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    ends_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Winner
    winner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    winner_points = Column(Integer, nullable=True)
    loser_points = Column(Integer, nullable=True)
    
    # Declined/Cancelled
    cancelled_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    cancellation_reason = Column(String(255), nullable=True)
    
    # Relationships
    challenger = relationship("User", foreign_keys=[challenger_id], back_populates="duels_challenged")
    opponent = relationship("User", foreign_keys=[opponent_id], back_populates="duels_received")
    winner = relationship("User", foreign_keys=[winner_id])
    events = relationship("DuelEvent", back_populates="duel", cascade="all, delete-orphan")


class DuelEvent(BaseModel):
    """Events/milestones during a duel."""
    __tablename__ = "duel_events"
    
    duel_id = Column(Integer, ForeignKey("duels.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Event details
    event_type = Column(String(50), nullable=False)  # progress_update, milestone, completion
    event_description = Column(String(255), nullable=True)
    
    # Progress data
    progress_value = Column(Float, nullable=True)  # Current progress toward goal
    total_value = Column(Float, nullable=True)  # Goal value
    percentage_complete = Column(Float, nullable=True)
    
    # Metadata
    metadata = Column(JSON, nullable=True)  # Context about the event
    
    # Timestamp
    recorded_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    duel = relationship("Duel", back_populates="events")
    user = relationship("User")


class DuelTemplate(BaseModel):
    """Reusable duel challenge templates."""
    __tablename__ = "duel_templates"
    
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    
    # Challenge type
    challenge_type = Column(String(50), nullable=False)
    challenge_subtype = Column(String(50), nullable=True)
    
    # Rules template
    default_rules = Column(JSON, nullable=False)  # {"goal": 100, "metric": "xp"}
    min_stakes = Column(Integer, default=0)
    max_stakes = Column(Integer, default=1000)
    
    # Time limits
    default_duration_hours = Column(Integer, default=24)
    min_duration_hours = Column(Integer, default=1)
    max_duration_hours = Column(Integer, default=168)  # 1 week
    
    # Settings
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    usage_count = Column(Integer, default=0)
    
    # Visual
    icon_url = Column(String(500), nullable=True)
    color_theme = Column(String(50), nullable=True)
