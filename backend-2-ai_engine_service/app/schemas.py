from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Profile(BaseModel):
    user_id: Optional[int] = None
    headline: Optional[str] = ""
    skills: Optional[List[str]] = []
    education: Optional[str] = ""
    experience_years: Optional[float] = 0.0
    location: Optional[str] = ""
    region: Optional[str] = ""
    preferred_language: Optional[str] = ""
    preferred_nsqf_level: Optional[int] = None

class MatchRequest(BaseModel):
    profile: Profile
    top_k: Optional[int] = 10
    filters: Optional[Dict[str, Any]] = None

class LearnerMatchRequest(BaseModel):
    skills: Optional[List[str]] = []
    experience_years: Optional[float] = 0.0
    preferred_nsqf_level: Optional[int] = None
    region: Optional[str] = ""
    preferred_language: Optional[str] = ""
    top_k: Optional[int] = 10
    filters: Optional[Dict[str, Any]] = None

class CoursePrediction(BaseModel):
    match_probability: float
    completion_probability: float
    performance_probability: float
    engagement_probability: float
    combined_score: float

class CourseMatch(BaseModel):
    course_id: str
    title: str
    description: str
    nsqf_level: int
    skills: str
    keywords: str
    duration_months: int
    language: str
    region: str
    _score: Optional[float] = None
    _final_score: Optional[float] = None

class CourseMatchResponse(BaseModel):
    course_id: str
    title: str
    description: str
    nsqf_level: int
    skills: str
    duration_months: int
    language: str
    region: str
    match_probability: float
    completion_probability: float
    performance_probability: float
    engagement_probability: float
    combined_score: float
    predictions: Dict[str, Any]

class CourseResponse(BaseModel):
    matches: List[Dict[str, Any]]
    total: int

class MonitorRequest(BaseModel):
    events: List[Dict[str, Any]]
    user_id: Optional[str] = None

class MonitorAlert(BaseModel):
    type: str
    severity: str
    message: str

class MonitorAnalysis(BaseModel):
    anomaly: Dict[str, Any]
    boredom: Dict[str, Any]
    inactivity: Dict[str, Any]
    struggle: Dict[str, Any]
    fast_completion: Dict[str, Any]

class MonitorResponse(BaseModel):
    overall_status: str
    alerts: List[MonitorAlert]
    analysis: MonitorAnalysis

class LearnerState(BaseModel):
    engagement_score: Optional[float] = 50.0
    performance_score: Optional[float] = 50.0
    completion_rate: Optional[float] = 50.0
    current_level: Optional[int] = 1
    streak_days: Optional[int] = 0

class AdaptiveRecommendRequest(BaseModel):
    learner_state: LearnerState
    available_courses: List[Dict[str, Any]]

class AdaptiveUpdateRequest(BaseModel):
    learner_state: LearnerState
    action: str
    feedback: Dict[str, Any]

class LearningStyleRequest(BaseModel):
    events: List[Dict[str, Any]]
