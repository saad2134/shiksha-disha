"""Core database module."""

from database.core.base import Base, BaseModel, IDMixin, TimestampMixin, SoftDeleteMixin
from database.core.enums import (
    ContentType, DifficultyLevel, BadgeCategory, BadgeRarity,
    ConnectionStatus, DuelStatus, ModuleStatus, NotificationType,
    PointsActionType, LearningStyle
)

__all__ = [
    'Base', 'BaseModel', 'IDMixin', 'TimestampMixin', 'SoftDeleteMixin',
    'ContentType', 'DifficultyLevel', 'BadgeCategory', 'BadgeRarity',
    'ConnectionStatus', 'DuelStatus', 'ModuleStatus', 'NotificationType',
    'PointsActionType', 'LearningStyle'
]
