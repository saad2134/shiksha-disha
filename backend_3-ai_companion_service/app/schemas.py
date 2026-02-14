from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Message(BaseModel):
    role: str
    content: str

class ConversationContext(BaseModel):
    user_id: Optional[str] = None
    skills: List[str] = []
    current_role: Optional[str] = None
    target_role: Optional[str] = None
    experience_years: float = 0.0
    interests: List[str] = []

class ChatRequest(BaseModel):
    message: str
    context: Optional[ConversationContext] = None
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    suggestions: List[str] = []
    resources: List[Dict[str, Any]] = []

class SkillForecastRequest(BaseModel):
    current_skills: List[str]
    industry: Optional[str] = None
    years_ahead: int = 3

class SkillForecastResponse(BaseModel):
    emerging_skills: List[Dict[str, Any]]
    declining_skills: List[Dict[str, Any]]
    recommended_focus: List[str]
    confidence: float

class AlertRequest(BaseModel):
    industry: Optional[str] = None
    region: Optional[str] = None

class IndustryAlert(BaseModel):
    id: str
    title: str
    description: str
    industry: str
    severity: str
    impact: str
    date: str

class RecommendationRequest(BaseModel):
    user_id: Optional[str] = None
    skills: List[str] = []
    current_course: Optional[str] = None
    interests: List[str] = []

class ContentRecommendation(BaseModel):
    title: str
    type: str
    relevance_score: float
    url: Optional[str] = None
    description: Optional[str] = None
