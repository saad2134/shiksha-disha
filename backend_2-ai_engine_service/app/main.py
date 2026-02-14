from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from .schemas import MatchRequest, Profile, CourseResponse, LearnerMatchRequest, CourseMatchResponse, MonitorRequest, MonitorResponse, AdaptiveRecommendRequest, AdaptiveUpdateRequest, LearningStyleRequest
from .matcher import semantic_search, apply_filters, compose_scores
from .indexer import build_index, load_index
from .config import settings
from .behavior_analyzer import analyzer
from .catalog import load_catalog
from .learner_course_matcher import matcher
from .learner_monitor import monitor
from .adaptive_recommender import recommender
from .learning_style_classifier import classifier
import uvicorn
import pandas as pd
from typing import Optional, List
from datetime import datetime

app = FastAPI(
    title="ShikshaDisha AI Engine Service",
    description="""
    ## 🎓 AI-Powered NSQF-Integrated Learning Ecosystem
    
    This service provides intelligent course matching and career pathway recommendations
    for learners based on their profile, skills, and preferences.
    
    ### Features:
    - **Semantic Course Matching** - AI-powered course recommendations
    - **Behavior Analysis** - Predict engagement and dropout risk
    - **NSQF Alignment** - National Skills Qualifications Framework integration
    - **Career Intelligence** - Personalized pathway recommendations
    
    ### API Version: 1.0.0
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "Matching", "description": "Course matching and pathway recommendations"},
        {"name": "Behavior", "description": "Learner behavior analysis and predictions"},
        {"name": "Courses", "description": "Course catalog endpoints"},
        {"name": "Admin", "description": "Administrative endpoints"}
    ]
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
        "service": "ShikshaDisha AI Engine",
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


@app.post("/match", response_model=CourseResponse, tags=["Matching"])
def match(req: MatchRequest):
    """
    Match courses to a learner profile using semantic search and filtering.
    
    - **profile**: Learner profile with skills, education, experience
    - **top_k**: Number of top matches to return (default: 10)
    - **filters**: Optional filters (nsqf_level, region, language, max_duration_months)
    """
    profile = req.profile.dict()
    sem = semantic_search(profile, top_k=200)
    filtered = apply_filters(sem, profile, filters=req.filters or {})
    scored = compose_scores(filtered, profile)
    return {"matches": scored[:req.top_k], "total": len(scored)}


@app.post("/match/simple", tags=["Matching"])
def match_simple(
    skills: List[str] = Query([]),
    headline: str = Query(""),
    education: str = Query(""),
    experience_years: float = Query(0.0),
    location: str = Query(""),
    region: str = Query(""),
    preferred_nsqf_level: int = Query(None),
    top_k: int = Query(10, ge=1, le=100)
):
    """Simple endpoint for quick course matching with query parameters."""
    profile = {
        "skills": skills,
        "headline": headline,
        "education": education,
        "experience_years": experience_years,
        "location": location,
        "region": region,
        "preferred_nsqf_level": preferred_nsqf_level
    }
    sem = semantic_search(profile, top_k=200)
    scored = compose_scores(sem, profile)
    return {"matches": scored[:top_k]}


@app.post("/match/learner", response_model=List[CourseMatchResponse], tags=["Matching"])
def match_learner(req: LearnerMatchRequest):
    """
    Match courses to a learner using logistic regression model.
    
    Predicts:
    - Match probability: How well the learner matches with the course
    - Completion probability: Likelihood of completing the course
    - Performance probability: Expected performance in the course
    - Engagement probability: Likelihood of staying engaged
    
    - **skills**: List of learner skills
    - **experience_years**: Years of experience
    - **preferred_nsqf_level**: Desired NSQF level
    - **region**: Preferred region
    - **preferred_language**: Preferred language
    - **top_k**: Number of top matches to return
    """
    profile = {
        "skills": req.skills or [],
        "experience_years": req.experience_years or 0.0,
        "preferred_nsqf_level": req.preferred_nsqf_level,
        "region": req.region or "",
        "preferred_language": req.preferred_language or ""
    }
    
    df = load_catalog()
    
    if req.filters:
        if 'nsqf_level' in req.filters:
            df = df[df['nsqf_level'] == req.filters['nsqf_level']]
        if 'region' in req.filters and req.filters['region']:
            df = df[df['region'].str.lower() == req.filters['region'].lower()]
        if 'language' in req.filters and req.filters['language']:
            df = df[df['language'].str.lower() == req.filters['language'].lower()]
        if 'max_duration_months' in req.filters:
            df = df[df['duration_months'] <= req.filters['max_duration_months']]
    
    courses = df.to_dict('records')
    matches = matcher.match_courses(profile, courses, top_k=req.top_k or 10)
    
    return matches


@app.post("/match/learner/predict", tags=["Matching"])
def predict_learner_course(
    skills: List[str] = Query([]),
    experience_years: float = Query(0.0),
    preferred_nsqf_level: int = Query(None),
    region: str = Query(""),
    preferred_language: str = Query(""),
    course_id: str = Query(...)
):
    """
    Get predictions for a specific course match for a learner.
    """
    profile = {
        "skills": skills,
        "experience_years": experience_years,
        "preferred_nsqf_level": preferred_nsqf_level,
        "region": region,
        "preferred_language": preferred_language
    }
    
    df = load_catalog()
    course = df[df['course_id'] == course_id]
    
    if course.empty:
        raise HTTPException(status_code=404, detail="Course not found")
    
    course_dict = course.iloc[0].to_dict()
    
    match_pred = matcher.predict_match(profile, course_dict)
    completion_pred = matcher.predict_completion(profile, course_dict)
    performance_pred = matcher.predict_performance(profile, course_dict)
    engagement_pred = matcher.predict_engagement(profile, course_dict)
    
    return {
        "course": course_dict,
        "predictions": {
            "match": match_pred,
            "completion": completion_pred,
            "performance": performance_pred,
            "engagement": engagement_pred
        }
    }


@app.post("/match/train", tags=["Matching"])
def train_matcher():
    """
    Train the logistic regression models for learner-course matching.
    """
    matcher.train()
    matcher.save()
    return {"ok": True, "message": "Learner-course matcher trained and saved successfully"}


@app.get("/courses", tags=["Courses"])
def list_courses(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    nsqf_level: Optional[int] = Query(None),
    region: Optional[str] = Query(None)
):
    """List all available NSQF courses with optional filtering."""
    df = load_catalog()
    
    if nsqf_level is not None:
        df = df[df['nsqf_level'] == nsqf_level]
    if region:
        df = df[df['region'].str.lower() == region.lower()]
    
    total = len(df)
    courses = df.iloc[offset:offset + limit].to_dict(orient='records')
    
    return {"courses": courses, "total": total, "limit": limit, "offset": offset}


@app.get("/courses/search", tags=["Courses"])
def search_courses(q: str = Query(..., min_length=2)):
    """Search courses by keyword."""
    df = load_catalog()
    mask = (
        df['title'].str.contains(q, case=False, na=False) |
        df['description'].str.contains(q, case=False, na=False) |
        df['skills'].str.contains(q, case=False, na=False) |
        df['keywords'].str.contains(q, case=False, na=False)
    )
    results = df[mask].head(20).to_dict(orient='records')
    return {"results": results, "count": len(results)}


@app.get("/course/{course_id}", tags=["Courses"])
def get_course(course_id: str):
    """Get detailed information about a specific course."""
    _, meta = load_index()
    for m in meta:
        if str(m.get('course_id')) == str(course_id):
            return m
    raise HTTPException(status_code=404, detail="Course not found")


@app.post("/admin/rebuild_index", tags=["Admin"])
def admin_rebuild():
    """Rebuild the FAISS index for course matching."""
    idx, meta = build_index(rebuild=True)
    return {"ok": True, "count": len(meta), "message": "Index rebuilt successfully"}


@app.get("/admin/stats", tags=["Admin"])
def admin_stats():
    """Get service statistics."""
    try:
        _, meta = load_index()
        course_count = len(meta)
    except:
        df = load_catalog()
        course_count = len(df)
    
    return {
        "courses_indexed": course_count,
        "embedding_model": settings.EMBEDDING_MODEL,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/behavior/analyze", tags=["Behavior"])
def analyze_behavior(request: dict):
    """
    Analyze learner behavior and provide recommendations.
    
    - **events**: List of learner events (page_view, click, scroll, pause, complete, etc.)
    """
    events = request.get('events', [])
    if not events:
        return {
            'engagement_score': 50,
            'dropout_probability': 0.5,
            'risk_level': 'medium',
            'recommendation': {
                'action': 'continue',
                'content_type': 'video',
                'reason': 'No behavior data available - defaulting to normal engagement'
            }
        }
    
    df = pd.DataFrame(events)
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    return analyzer.get_recommendation(df)


@app.post("/behavior/engagement", tags=["Behavior"])
def predict_engagement(request: dict):
    """Predict learner engagement score based on behavior events."""
    events = request.get('events', [])
    if not events:
        return {'engagement_score': 50, 'confidence': 0}
    
    df = pd.DataFrame(events)
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    return analyzer.predict_engagement(df)


@app.post("/behavior/dropout", tags=["Behavior"])
def predict_dropout(request: dict):
    """Predict learner dropout risk based on behavior events."""
    events = request.get('events', [])
    if not events:
        return {'dropout_probability': 0.5, 'risk_level': 'medium'}
    
    df = pd.DataFrame(events)
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    return analyzer.predict_dropout(df)


@app.post("/behavior/train", tags=["Behavior"])
def train_behavior_model():
    """Train the behavior analysis models."""
    analyzer.train()
    analyzer.save()
    return {'ok': True, 'message': 'Model trained and saved successfully'}


@app.post("/monitor/analyze", response_model=MonitorResponse, tags=["Monitoring"])
def monitor_analyze(request: MonitorRequest):
    """
    Analyze learner session for anomalies and issues.
    
    Detects:
    - Boredom patterns (low interaction, long gaps)
    - Inactivity (long inactive periods)
    - Struggle (tab switching, quiz failures, video pausing)
    - Fast completion (suspiciously quick completion)
    
    - **events**: List of learner events with timestamps
    - **user_id**: Optional user identifier
    """
    return monitor.analyze_session(request.events, request.user_id)


@app.post("/monitor/boredom", tags=["Monitoring"])
def detect_boredom(request: MonitorRequest):
    """
    Detect if user is bored or disengaged.
    """
    return monitor.detect_boredom(request.events)


@app.post("/monitor/inactivity", tags=["Monitoring"])
def detect_inactivity(request: MonitorRequest):
    """
    Detect long inactive periods.
    """
    return monitor.detect_inactivity(request.events)


@app.post("/monitor/struggle", tags=["Monitoring"])
def detect_struggle(request: MonitorRequest):
    """
    Detect if user is struggling with content.
    """
    return monitor.detect_struggle(request.events)


@app.post("/monitor/fast-completion", tags=["Monitoring"])
def detect_fast_completion(request: MonitorRequest):
    """
    Detect suspicious fast completion patterns.
    """
    return monitor.detect_fast_completion(request.events)


@app.post("/monitor/recommendations", tags=["Monitoring"])
def get_monitor_recommendations(request: MonitorRequest):
    """
    Get actionable recommendations based on learner behavior.
    """
    return {'recommendations': monitor.get_recommendations(request.events)}


@app.post("/monitor/train", tags=["Monitoring"])
def train_monitor():
    """Train the learner monitoring models."""
    monitor.train()
    monitor.save()
    return {'ok': True, 'message': 'Monitor models trained and saved successfully'}


@app.post("/adaptive/recommend", tags=["Adaptive"])
def adaptive_recommend(request: AdaptiveRecommendRequest):
    """
    Get adaptive course recommendations using reinforcement learning.
    
    The model learns from user feedback to improve recommendations over time.
    """
    learner_state = request.learner_state.dict()
    courses = request.available_courses
    
    return recommender.get_recommendation(learner_state, courses)


@app.post("/adaptive/update", tags=["Adaptive"])
def adaptive_update(request: AdaptiveUpdateRequest):
    """
    Update the reinforcement learning model with user feedback.
    
    Feedback can include:
    - engagement_delta: Change in engagement score
    - completion: Whether user completed the course
    - performance_delta: Change in performance
    - satisfaction: User satisfaction (0-1)
    - skip: Whether user skipped the recommendation
    - negative_feedback: User gave negative feedback
    """
    learner_state = request.learner_state.dict()
    result = recommender.update(learner_state, request.action, request.feedback)
    recommender.save()
    return result


@app.get("/adaptive/stats", tags=["Adaptive"])
def adaptive_stats():
    """Get adaptive recommendation system statistics."""
    return recommender.get_stats()


@app.get("/adaptive/policy", tags=["Adaptive"])
def adaptive_policy():
    """Get the current learned policy from Q-table."""
    return {'policy': recommender.get_policy()}


@app.post("/learning-style/predict", tags=["Learning Style"])
def predict_learning_style(request: LearningStyleRequest):
    """
    Predict learner's learning style based on their behavior.
    
    Learning styles: visual, auditory, reading_writing, kinesthetic
    """
    return classifier.predict(request.events)


@app.post("/learning-style/recommendations", tags=["Learning Style"])
def get_style_recommendations(learning_style: str = Query(...)):
    """Get content recommendations based on learning style."""
    return classifier.get_style_recommendations(learning_style)


@app.get("/learning-style/importance", tags=["Learning Style"])
def get_feature_importance():
    """Get feature importance for learning style classification."""
    return {'importance': classifier.get_feature_importance()}


@app.post("/learning-style/train", tags=["Learning Style"])
def train_classifier():
    """Train the learning style classifier."""
    classifier.train()
    classifier.save()
    return {'ok': True, 'message': 'Learning style classifier trained successfully'}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
