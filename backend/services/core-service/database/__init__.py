"""ShikshaDisha Database Module

Complete database schema for the AI-powered NSQF learning platform.
"""

# Core
from database.core import Base, BaseModel

# Users
from database.users import User, UserDevice

# Engagement
from database.engagement import (
    DailyLogin, LearningSession, BehaviorEvent, UserEngagementProfile,
    AttentionSpan, FocusPattern
)

# Gamification
from database.gamification import (
    UserStreak, StreakActivity, Badge, UserBadge, 
    UserPoints, PointsTransaction, Leaderboard, Duel
)

# Learning
from database.learning import (
    Skill, SkillMastery, LearningPath, PathModule,
    Quiz, QuizAttempt, LearningPreference
)

# Social
from database.social import UserConnection, StudyGroup, SocialActivity

# Notifications
from database.notifications import Notification, NotificationPreference

# Analytics
from database.analytics import DailyMetrics, MLFeatureStore

__version__ = "1.0.0"

# Convenience function to create all tables
def create_all_tables(engine):
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)

# Convenience function to drop all tables
def drop_all_tables(engine):
    """Drop all database tables."""
    Base.metadata.drop_all(bind=engine)

__all__ = [
    # Core
    'Base', 'BaseModel', 'create_all_tables', 'drop_all_tables',
    
    # Users
    'User', 'UserDevice',
    
    # Engagement
    'DailyLogin', 'LearningSession', 'BehaviorEvent', 'UserEngagementProfile',
    'AttentionSpan', 'FocusPattern',
    
    # Gamification
    'UserStreak', 'StreakActivity', 'Badge', 'UserBadge',
    'UserPoints', 'PointsTransaction', 'Leaderboard', 'Duel',
    
    # Learning
    'Skill', 'SkillMastery', 'LearningPath', 'PathModule',
    'Quiz', 'QuizAttempt', 'LearningPreference',
    
    # Social
    'UserConnection', 'StudyGroup', 'SocialActivity',
    
    # Notifications
    'Notification', 'NotificationPreference',
    
    # Analytics
    'DailyMetrics', 'MLFeatureStore',
]
