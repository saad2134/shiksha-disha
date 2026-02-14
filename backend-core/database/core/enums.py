"""Common enums used across the database."""

from enum import Enum as PyEnum


class ContentType(str, PyEnum):
    """Types of learning content."""
    VIDEO = "video"
    AUDIO = "audio"
    TEXT = "text"
    INTERACTIVE = "interactive"
    QUIZ = "quiz"
    SIMULATION = "simulation"


class DifficultyLevel(str, PyEnum):
    """Difficulty levels for content."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class BadgeCategory(str, PyEnum):
    """Categories for badges/achievements."""
    STREAK = "streak"
    SKILL = "skill"
    SOCIAL = "social"
    EXPLORER = "explorer"
    ACHIEVEMENT = "achievement"


class BadgeRarity(str, PyEnum):
    """Rarity levels for badges."""
    COMMON = "common"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


class ConnectionStatus(str, PyEnum):
    """Status for user connections."""
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    BLOCKED = "blocked"


class DuelStatus(str, PyEnum):
    """Status for duels/challenges."""
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class ModuleStatus(str, PyEnum):
    """Status for learning modules."""
    LOCKED = "locked"
    AVAILABLE = "available"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"


class NotificationType(str, PyEnum):
    """Types of notifications."""
    STREAK_REMINDER = "streak_reminder"
    ACHIEVEMENT_UNLOCKED = "achievement_unlocked"
    PATH_UPDATE = "path_update"
    DUEL_CHALLENGE = "duel_challenge"
    SOCIAL = "social"
    SYSTEM = "system"


class PointsActionType(str, PyEnum):
    """Types of actions that award points."""
    LOGIN_STREAK = "login_streak"
    COURSE_COMPLETE = "course_complete"
    MODULE_COMPLETE = "module_complete"
    QUIZ_PERFECT = "quiz_perfect"
    SKILL_MASTERED = "skill_mastered"
    STREAK_MILESTONE = "streak_milestone"
    BADGE_EARNED = "badge_earned"
    DUEL_WON = "duel_won"
    SOCIAL_SHARE = "social_share"


class LearningStyle(str, PyEnum):
    """VARK learning styles."""
    VISUAL = "visual"
    AUDITORY = "auditory"
    READING = "reading"
    KINESTHETIC = "kinesthetic"
    MULTIMODAL = "multimodal"
