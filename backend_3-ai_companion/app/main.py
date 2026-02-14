from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from .schemas import (
    ChatRequest, ChatResponse, ChatResponse,
    SkillForecastRequest, SkillForecastResponse,
    AlertRequest, IndustryAlert,
    RecommendationRequest, ContentRecommendation
)
from .chatbot import companion
from .skill_forecast import forecaster
from .alerts import alert_manager
from .recommender import recommender
from datetime import datetime
from typing import List, Optional
import uuid

app = FastAPI(
    title="ShikshaDisha AI Companion",
    description="""
    ## 🤖 AI Learning Companion
    
    Your personal AI guide for career development, skill forecasting, 
    and learning recommendations.
    
    ### Features:
    - **Intelligent Chat** - Real-time career and learning guidance
    - **Skill Forecasting** - Predict emerging and declining skills
    - **Industry Alerts** - Stay updated on market trends
    - **Content Recommendations** - Personalized learning resources
    
    ### API Version: 1.0.0
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
def root():
    return {
        "service": "ShikshaDisha AI Companion",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "operational"
    }


@app.get("/health", tags=["Root"])
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
def chat(request: ChatRequest):
    """
    Chat with the AI Companion for career guidance and learning recommendations.
    
    - **message**: Your question or message
    - **context**: Optional user context (skills, experience, interests)
    - **conversation_id**: Optional to continue an existing conversation
    """
    context_dict = request.context.dict() if request.context else None
    result = companion.chat(
        message=request.message,
        context=context_dict,
        conversation_id=request.conversation_id
    )
    return result


@app.post("/chat/new", tags=["Chat"])
def new_conversation(user_id: Optional[str] = Query(None)):
    """Start a new conversation with the AI Companion."""
    conv_id = companion.conversation_manager.create_conversation(user_id)
    return {
        "conversation_id": conv_id,
        "message": "New conversation started. How can I help you today?"
    }


@app.get("/chat/{conversation_id}/history", tags=["Chat"])
def get_conversation_history(conversation_id: str, limit: int = Query(50, ge=1, le=100)):
    """Get the history of a conversation."""
    history = companion.conversation_manager.get_conversation(conversation_id)
    return {
        "conversation_id": conversation_id,
        "messages": history[-limit:],
        "total": len(history)
    }


@app.delete("/chat/{conversation_id}", tags=["Chat"])
def clear_conversation(conversation_id: str):
    """Clear a conversation history."""
    companion.conversation_manager.clear_conversation(conversation_id)
    return {"message": "Conversation cleared successfully"}


@app.post("/forecast", tags=["Skill Forecast"])
def forecast_skills(request: SkillForecastRequest):
    """
    Get skill forecast based on current skills and industry.
    
    - **current_skills**: List of skills you currently have
    - **industry**: Target industry (technology, healthcare, finance, marketing)
    - **years_ahead**: How many years to forecast (1-5)
    """
    return forecaster.forecast(
        current_skills=request.current_skills,
        industry=request.industry,
        years_ahead=request.years_ahead
    )


@app.get("/forecast/sample/{industry}", tags=["Skill Forecast"])
def sample_forecast(industry: str = "technology", years_ahead: int = Query(3, ge=1, le=5)):
    """Get sample skill forecast for an industry."""
    sample_skills = {
        "technology": ["python", "javascript", "sql"],
        "healthcare": ["patient care", "medical terminology"],
        "finance": ["accounting", "excel", "financial analysis"],
        "marketing": ["social media", "content writing", "analytics"]
    }
    skills = sample_skills.get(industry.lower(), ["communication", "problem solving"])
    return forecaster.forecast(skills, industry, years_ahead)


@app.get("/alerts", tags=["Industry Alerts"])
def get_alerts(
    industry: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=50),
    severity: Optional[str] = Query(None)
):
    """
    Get industry alerts and market trends.
    
    - **industry**: Filter by industry (technology, healthcare, finance, marketing)
    - **region**: Filter by region
    - **limit**: Number of alerts to return
    - **severity**: Filter by severity (high, medium, low)
    """
    if severity:
        alerts = alert_manager.get_alerts_by_severity(severity)
    else:
        alerts = alert_manager.get_alerts(industry, region, limit)
    
    return {"alerts": alerts, "count": len(alerts)}


@app.get("/alerts/high-priority", tags=["Industry Alerts"])
def get_high_priority_alerts():
    """Get all high-priority industry alerts."""
    alerts = alert_manager.get_high_priority_alerts()
    return {"alerts": alerts, "count": len(alerts)}


@app.get("/alerts/{alert_id}", tags=["Industry Alerts"])
def get_alert(alert_id: str):
    """Get a specific alert by ID."""
    alert = alert_manager.get_alert_by_id(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@app.post("/recommend", tags=["Content Recommendations"])
def recommend_content(request: RecommendationRequest):
    """
    Get personalized content recommendations.
    
    - **skills**: User's current skills
    - **interests**: Areas of interest
    - **current_course**: Course to exclude from recommendations
    """
    recommendations = recommender.recommend(
        skills=request.skills,
        interests=request.interests,
        current_course=request.current_course,
        limit=10
    )
    return {"recommendations": recommendations, "count": len(recommendations)}


@app.get("/recommend/courses", tags=["Content Recommendations"])
def get_courses(
    level: Optional[str] = Query(None),
    content_type: str = Query("course"),
    limit: int = Query(20, ge=1, le=50)
):
    """Get available courses with optional filtering."""
    courses = recommender.recommend_by_type(content_type, level, limit)
    return {"courses": courses, "count": len(courses)}


@app.get("/recommend/search", tags=["Content Recommendations"])
def search_content(q: str = Query(..., min_length=2), limit: int = Query(10, ge=1, le=50)):
    """Search for content by keyword."""
    results = recommender.search(q, limit)
    return {"results": results, "count": len(results)}


@app.get("/resources", tags=["Resources"])
def get_resources():
    """Get all available learning resources."""
    return {
        "courses": recommender.recommend_by_type("course", limit=20),
        "workshops": recommender.recommend_by_type("workshop", limit=20),
        "total": len(CONTENT_DATABASE)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9001)


from .recommender import CONTENT_DATABASE
