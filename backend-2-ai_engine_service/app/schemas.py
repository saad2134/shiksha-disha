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

class CourseResponse(BaseModel):
    matches: List[Dict[str, Any]]
    total: int
