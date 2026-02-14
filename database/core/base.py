"""Core base classes and utilities for all database models."""

from sqlalchemy import create_engine, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declared_attr
from datetime import datetime

# Create base class
Base = declarative_base()


class TimestampMixin:
    """Mixin to add created_at and updated_at columns."""
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class SoftDeleteMixin:
    """Mixin to add soft delete capability."""
    
    is_deleted = Column(Integer, default=0)  # 0 = active, 1 = deleted
    deleted_at = Column(DateTime, nullable=True)


class IDMixin:
    """Mixin to add standard id column."""
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)


class BaseModel(IDMixin, TimestampMixin, SoftDeleteMixin):
    """Base model with all common mixins."""
    
    __abstract__ = True
