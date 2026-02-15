from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class LoginRequest(BaseModel):
    email: str
    password: str

class SignupRequest(BaseModel):
    email: str
    password: str
    name: str
    language: Optional[str] = "en"

class AuthResponse(BaseModel):
    success: bool
    message: str
    user: Optional[Dict[str, Any]] = None
    token: Optional[str] = None

class UserCreate(BaseModel):
    email: str
    name: Optional[str] = None
    language: Optional[str] = "en"

class UserOut(BaseModel):
    id: int
    email: str
    name: Optional[str]
    language: str
    created_at: datetime
    education: Optional[str] = None
    field_of_study: Optional[str] = None
    skills: List[Any] = []
    interests: List[Any] = []
    learning_goals: List[Any] = []
    target_roles: Optional[str] = None
    learning_types: List[Any] = []
    video_format: Optional[str] = None
    learning_style: Optional[str] = None
    instructor_style: Optional[str] = None
    course_structure: Optional[str] = None
    theory_practice_ratio: Optional[str] = None
    math_intensity: Optional[str] = None
    learning_environment: List[Any] = []
    internet_situation: List[Any] = []
    collaborative_learning: Optional[str] = None
    comfortable_subjects: List[Any] = []
    familiar_with: List[Any] = []
    certifications: Optional[str] = None
    resume_url: Optional[str] = None
    preferred_nsqf_level: int = 4
    region: Optional[str] = None
    career_goal: Optional[str] = None
    progress: int = 0
    courses_completed: int = 0
    skills_gained: int = 0
    weeks_remaining: int = 12
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    language: Optional[str] = None
    education: Optional[str] = None
    field_of_study: Optional[str] = None
    skills: Optional[List[Any]] = None
    interests: Optional[List[Any]] = None
    learning_goals: Optional[List[Any]] = None
    target_roles: Optional[str] = None
    learning_types: Optional[List[Any]] = None
    video_format: Optional[str] = None
    learning_style: Optional[str] = None
    instructor_style: Optional[str] = None
    course_structure: Optional[str] = None
    theory_practice_ratio: Optional[str] = None
    math_intensity: Optional[str] = None
    learning_environment: Optional[List[Any]] = None
    internet_situation: Optional[List[Any]] = None
    collaborative_learning: Optional[str] = None
    comfortable_subjects: Optional[List[Any]] = None
    familiar_with: Optional[List[Any]] = None
    certifications: Optional[str] = None
    resume_url: Optional[str] = None
    preferred_nsqf_level: Optional[int] = None
    region: Optional[str] = None
    career_goal: Optional[str] = None
    progress: Optional[int] = None
    courses_completed: Optional[int] = None
    skills_gained: Optional[int] = None
    weeks_remaining: Optional[int] = None


class OnboardingData(BaseModel):
    fullName: Optional[str] = None
    contact: Optional[str] = None
    education: Optional[str] = None
    fieldOfStudy: Optional[str] = None
    comfortableSubjects: Optional[List[str]] = None
    skills: Optional[List[str]] = None
    interests: Optional[List[str]] = None
    learningGoals: Optional[List[str]] = None
    learningTypes: Optional[List[str]] = None
    videoFormat: Optional[str] = None
    learningStyle: Optional[str] = None
    instructorStyle: Optional[str] = None
    courseStructure: Optional[str] = None
    theoryPracticeRatio: Optional[str] = None
    mathIntensity: Optional[str] = None
    learningEnvironment: Optional[List[str]] = None
    internetSituation: Optional[List[str]] = None
    collaborativeLearning: Optional[str] = None
    familiarWith: Optional[List[str]] = None
    certifications: Optional[str] = None
    resumeUrl: Optional[str] = None
    targetRoles: Optional[str] = None
    preferredLanguage: Optional[str] = "en"
    region: Optional[str] = None
    careerGoal: Optional[str] = None


class UserStats(BaseModel):
    progress: int = 0
    courses_completed: int = 0
    skills_gained: int = 0
    weeks_remaining: int = 12
    current_streak: int = 0
    engagement_score: float = 0.0
    dropout_risk: float = 0.0

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
    model_config = {"from_attributes": True}

class NotificationCreate(BaseModel):
    user_id: int
    title: str
    body: str
    meta: Optional[Dict[str, Any]] = None
    deliver_immediately: Optional[bool] = True

class NotificationOut(BaseModel):
    id: int
    user_id: int
    title: str
    body: str
    meta: Optional[Dict[str, Any]]
    delivered: bool
    read: bool
    created_at: datetime
    class Config:
        from_attributes = True


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
    model_config = {"from_attributes": True}

class BehaviorEventCreate(BaseModel):
    user_id: int
    session_id: Optional[int] = None
    event_type: str
    content_id: Optional[str] = None
    content_type: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None

class BehaviorEventOut(BaseModel):
    id: int
    user_id: int
    session_id: Optional[int]
    event_type: str
    content_id: Optional[str]
    content_type: Optional[str]
    meta: Optional[Dict[str, Any]]
    timestamp: datetime
    class Config:
        from_attributes = True

class EngagementProfileOut(BaseModel):
    user_id: int
    avg_engagement_score: float
    preferred_content_type: Optional[str]
    preferred_difficulty: Optional[str]
    dropout_risk_score: float
    last_updated: datetime
    model_config = {"from_attributes": True}

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
    model_config = {"from_attributes": True}


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
    model_config = {"from_attributes": True}
