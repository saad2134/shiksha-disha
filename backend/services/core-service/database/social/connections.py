"""Social connections models."""

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database.core.base import BaseModel
from database.core.enums import ConnectionStatus


class UserConnection(BaseModel):
    """Connections between users (friends, study buddies)."""
    __tablename__ = "user_connections"
    
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    addressee_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Status
    status = Column(Enum(ConnectionStatus), default=ConnectionStatus.PENDING)
    
    # Request details
    message = Column(Text, nullable=True)  # Optional message with request
    requested_at = Column(DateTime, default=datetime.utcnow)
    responded_at = Column(DateTime, nullable=True)
    
    # Connection stats
    connected_at = Column(DateTime, nullable=True)
    study_sessions_together = Column(Integer, default=0)
    last_interaction_at = Column(DateTime, nullable=True)
    
    # Relationship quality (AI-calculated)
    interaction_score = Column(Float, nullable=True)  # How well they study together
    compatibility_score = Column(Float, nullable=True)
    
    # Relationships
    requester = relationship("User", foreign_keys=[requester_id], back_populates="connections_sent")
    addressee = relationship("User", foreign_keys=[addressee_id], back_populates="connections_received")


class ConnectionInteraction(BaseModel):
    """Track interactions between connected users."""
    __tablename__ = "connection_interactions"
    
    connection_id = Column(Integer, ForeignKey("user_connections.id"), nullable=False)
    initiator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Interaction details
    interaction_type = Column(String(50), nullable=False)  # message, study_invite, duel_challenge, resource_share
    content = Column(Text, nullable=True)
    
    # Status
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
