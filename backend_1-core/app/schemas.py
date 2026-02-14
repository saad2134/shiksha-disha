from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any, List
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    language: Optional[str] = "en"

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: Optional[str]
    language: str
    created_at: datetime
    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    language: Optional[str] = None

class ActionCreate(BaseModel):
    user_id: int
    type: str
    payload: Optional[Dict[str, Any]] = None

class ActionOut(BaseModel):
    id: int
    user_id: int
    type: str
    payload: Optional[Dict[str, Any]]
    created_at: datetime
    class Config:
        orm_mode = True

class NotificationCreate(BaseModel):
    user_id: int
    title: str
    body: str
    metadata: Optional[Dict[str, Any]] = None
    deliver_immediately: Optional[bool] = True

class NotificationOut(BaseModel):
    id: int
    user_id: int
    title: str
    body: str
    metadata: Optional[Dict[str, Any]]
    delivered: bool
    read: bool
    created_at: datetime
    class Config:
        orm_mode = True


class SessionStart(BaseModel):
    user_id: int
    content_id: str
    content_type: str

class SessionEnd(BaseModel):
    session_id: int
    duration_seconds: int = 0
    engagement_score: Optional[int] = None

class SessionOut(BaseModel):
    id: int
    user_id: int
    content_id: Optional[str]
    content_type: Optional[str]
    started_at: datetime
    ended_at: Optional[datetime]
    duration_seconds: int
    engagement_score: Optional[int]
    dropout_risk: Optional[float]
    class Config:
        orm_mode = True

class BehaviorEventCreate(BaseModel):
    user_id: int
    session_id: Optional[int] = None
    event_type: str
    content_id: Optional[str] = None
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class BehaviorEventOut(BaseModel):
    id: int
    user_id: int
    session_id: Optional[int]
    event_type: str
    content_id: Optional[str]
    content_type: Optional[str]
    metadata: Optional[Dict[str, Any]]
    timestamp: datetime
    class Config:
        orm_mode = True

class EngagementProfileOut(BaseModel):
    user_id: int
    avg_engagement_score: float
    preferred_content_type: Optional[str]
    preferred_difficulty: Optional[str]
    dropout_risk_score: float
    last_updated: datetime
    class Config:
        orm_mode = True

class RealtimePrediction(BaseModel):
    user_id: int
    session_id: Optional[int] = None
    current_engagement: float
    dropout_probability: float
    recommended_action: str
    content_type_suggestion: Optional[str] = None


class StreakOut(BaseModel):
    id: int
    user_id: int
    current_streak: int
    longest_streak: int
    last_activity_date: Optional[datetime]
    streak_start_date: Optional[datetime]
    total_active_days: int
    freeze_count: int
    updated_at: datetime
    class Config:
        orm_mode = True


class StreakActivityCreate(BaseModel):
    user_id: int
    minutes_active: int = 0
    sessions_completed: int = 0
    content_type: Optional[str] = None


class StreakActivityOut(BaseModel):
    id: int
    user_id: int
    activity_date: datetime
    minutes_active: int
    sessions_completed: int
    content_type: Optional[str]
    streak_continued: bool
    created_at: datetime
    class Config:
        orm_mode = True
