from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from .schemas import MatchRequest, Profile, CourseResponse
from .matcher import semantic_search, apply_filters, compose_scores
from .indexer import build_index, load_index
from .config import settings
from .behavior_analyzer import analyzer
from .catalog import load_catalog
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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
