# Database Schema Structure

This directory contains all database models organized by domain for the ShikshaDisha learning platform.

## Directory Structure

```
database/
├── README.md                          # This file
├── migrations/                        # Alembic/Flyway migrations
│   ├── versions/
│   └── env.py
│
├── core/                              # Base and utility models
│   ├── __init__.py
│   ├── base.py                        # SQLAlchemy Base class
│   ├── mixins.py                      # Common model mixins (timestamp, etc.)
│   └── enums.py                       # Enum definitions
│
├── users/                             # User management
│   ├── __init__.py
│   ├── models.py                      # User, UserProfile
│   └── schemas.py                     # Pydantic schemas
│
├── engagement/                        # User engagement tracking
│   ├── __init__.py
│   ├── daily_login.py                 # DailyLogin model
│   ├── learning_session.py            # LearningSession, SessionEvent
│   ├── attention_span.py              # AttentionSpan, FocusMetrics
│   └── behavior.py                    # BehaviorEvent, UserEngagementProfile
│
├── gamification/                      # Gamification system
│   ├── __init__.py
│   ├── streaks.py                     # UserStreak, StreakActivity, StreakFreeze
│   ├── badges.py                      # Badge, UserBadge, StreakMilestone
│   ├── points.py                      # UserPoints, PointsTransaction
│   ├── leaderboards.py                # Leaderboard, LeaderboardEntry
│   └── duels.py                       # Duel, DuelParticipant
│
├── learning/                          # Learning content & progress
│   ├── __init__.py
│   ├── skills.py                      # Skill, SkillMastery
│   ├── paths.py                       # LearningPath, PathModule
│   ├── assessments.py                 # QuizAttempt, AssessmentResult
│   └── preferences.py                 # LearningPreference, ContentPreference
│
├── social/                            # Social features
│   ├── __init__.py
│   ├── connections.py                 # UserConnection
│   ├── study_groups.py                # StudyGroup, GroupMember
│   └── activities.py                  # SocialActivity, ActivityFeed
│
├── notifications/                     # Notification system
│   ├── __init__.py
│   ├── models.py                      # Notification, NotificationPreference
│   └── templates.py                   # NotificationTemplate
│
└── analytics/                         # Analytics & reporting
    ├── __init__.py
    ├── metrics.py                     # Aggregated metrics
    ├── reports.py                     # Report definitions
    └── ml_features.py                 # ML feature store
```

## Model Relationships Overview

```
User (1)
  ├── Engagement (n) → daily_logins, sessions, behavior_events
  ├── Gamification (1:1/n) → streak, points, badges, duels
  ├── Learning (n) → skill_mastery, learning_paths, quiz_attempts
  ├── Social (n) → connections, groups
  └── Notifications (n) → notifications
```

## Key Design Principles

1. **Separation of Concerns**: Each module handles one domain
2. **Circular Import Safety**: Use string references for relationships
3. **Schema Co-location**: Pydantic schemas live with their models
4. **Migration Safety**: All changes go through Alembic migrations
5. **Indexing Strategy**: Frequent query fields are indexed

## Usage

```python
# Import specific models
from database.users.models import User
from database.gamification.streaks import UserStreak
from database.learning.skills import SkillMastery

# Or import all
from database import User, UserStreak, SkillMastery
```
