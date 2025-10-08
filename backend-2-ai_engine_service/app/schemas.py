from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Profile(BaseModel):
    user_id: Optional[int]
    headline: Optional[str]
    skills: Optional[List[str]] = []
    education: Optional[str] = None
    experience_years: Optional[float] = 0.0
    location: Optional[str] = None
    region: Optional[str] = None
    preferred_language: Optional[str] = None
    preferred_nsqf_level: Optional[int] = None

class MatchRequest(BaseModel):
    profile: Profile
    top_k: Optional[int] = 10
    filters: Optional[Dict[str, Any]] = None
