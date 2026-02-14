# Database Entity Relationship Diagram

## Core Entities

```
┌─────────────────────────────────────────────────────────────────────────┐
│                               USERS                                     │
├─────────────────────────────────────────────────────────────────────────┤
│  User                                                                   │
│  ├── UserDevice                                                         │
│  └── EngagementProfile                                                  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ relationships
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           ENGAGEMENT                                    │
├─────────────────────────────────────────────────────────────────────────┤
│  DailyLogin                                                             │
│  LearningSession                                                        │
│  ├── AttentionSpan                                                      │
│  └── BehaviorEvent                                                      │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          GAMIFICATION                                   │
├─────────────────────────────────────────────────────────────────────────┤
│  UserStreak                                                             │
│  ├── StreakActivity                                                     │
│  ├── StreakFreeze                                                       │
│  └── StreakMilestone                                                    │
│                                                                         │
│  UserPoints                                                             │
│  └── PointsTransaction                                                  │
│                                                                         │
│  Badge ←── UserBadge                                                    │
│                                                                         │
│  Leaderboard                                                            │
│  └── LeaderboardEntry                                                   │
│                                                                         │
│  Duel                                                                   │
│  └── DuelEvent                                                          │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                            LEARNING                                     │
├─────────────────────────────────────────────────────────────────────────┤
│  Skill                                                                  │
│  └── SkillMastery                                                       │
│                                                                         │
│  LearningPath                                                           │
│  ├── PathModule                                                         │
│  └── PathAdaptation                                                     │
│                                                                         │
│  Quiz ←── QuizAttempt                                                   │
│                                                                         │
│  Assessment ←── AssessmentSubmission                                    │
│                                                                         │
│  LearningPreference                                                     │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                            SOCIAL                                       │
├─────────────────────────────────────────────────────────────────────────┤
│  UserConnection                                                         │
│  └── ConnectionInteraction                                              │
│                                                                         │
│  StudyGroup                                                             │
│  ├── GroupMember                                                        │
│  └── GroupStudySession                                                  │
│      └── GroupSessionParticipant                                        │
│                                                                         │
│  SocialActivity                                                         │
│  ├── ActivityLike                                                       │
│  └── ActivityComment                                                    │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         NOTIFICATIONS                                   │
├─────────────────────────────────────────────────────────────────────────┤
│  Notification                                                           │
│  NotificationPreference                                                 │
│  └── NotificationCategorySetting                                        │
│  NotificationTemplate                                                   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           ANALYTICS                                     │
├─────────────────────────────────────────────────────────────────────────┤
│  DailyMetrics                                                           │
│  UserAnalytics                                                          │
│  ContentAnalytics                                                       │
│  ABTest                                                                 │
│  └── ABTestAssignment                                                   │
│  MLFeatureStore                                                         │
│  MLModelVersion                                                         │
│  MLPredictionLog                                                        │
│  RecommendationLog                                                      │
└─────────────────────────────────────────────────────────────────────────┘
```

## Key Relationships

```
User (1) ──────── (*) DailyLogin
User (1) ──────── (*) LearningSession
User (1) ──────── (*) BehaviorEvent
User (1) ──────── (*) AttentionSpan

User (1) ──────── (1) UserStreak
User (1) ──────── (*) StreakActivity
User (1) ──────── (1) UserPoints
User (1) ──────── (*) PointsTransaction
User (1) ──────── (*) UserBadge
User (1) ──────── (*) Duel

User (1) ──────── (*) SkillMastery
User (1) ──────── (*) LearningPath
User (1) ──────── (*) QuizAttempt
User (1) ──────── (1) LearningPreference

User (1) ──────── (*) UserConnection
User (1) ──────── (*) GroupMember
User (1) ──────── (*) SocialActivity

User (1) ──────── (*) Notification
User (1) ──────── (1) NotificationPreference
```

## Table Count Summary

| Domain | Tables |
|--------|--------|
| Core | 4 (base classes, enums) |
| Users | 2 |
| Engagement | 7 |
| Gamification | 14 |
| Learning | 15 |
| Social | 8 |
| Notifications | 4 |
| Analytics | 9 |
| **Total** | **~50+ tables** |
