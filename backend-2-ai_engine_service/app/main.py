from fastapi import FastAPI, HTTPException
from .schemas import MatchRequest
from .matcher import semantic_search, apply_filters, compose_scores
from .indexer import build_index
from .config import settings
from .behavior_analyzer import analyzer
import uvicorn
import pandas as pd
from datetime import datetime

app = FastAPI(title="ShikshaDisha - AI Matching Engine")

@app.post("/match")
def match(req: MatchRequest):
    profile = req.profile.dict()
    sem = semantic_search(profile, top_k=200)
    filtered = apply_filters(sem, profile, filters=req.filters or {})
    scored = compose_scores(filtered, profile)
    return {"matches": scored[:req.top_k]}

@app.post("/admin/rebuild_index")
def admin_rebuild():
    idx, meta = build_index(rebuild=True)
    return {"ok": True, "count": len(meta)}

@app.get("/course/{course_id}")
def get_course(course_id: str):
    from .indexer import load_index
    _, meta = load_index()
    for m in meta:
        if str(m.get('course_id')) == str(course_id):
            return m
    raise HTTPException(status_code=404, detail="course not found")


@app.post("/behavior/predict")
def predict_behavior(request: dict):
    events = request.get('events', [])
    if not events:
        return {'error': 'No events provided', 'engagement_score': 50, 'dropout_probability': 0.5}
    
    df = pd.DataFrame(events)
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    result = analyzer.get_recommendation(df)
    return result


@app.post("/behavior/engagement")
def predict_engagement(request: dict):
    events = request.get('events', [])
    if not events:
        return {'engagement_score': 50, 'confidence': 0}
    
    df = pd.DataFrame(events)
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    return analyzer.predict_engagement(df)


@app.post("/behavior/dropout")
def predict_dropout(request: dict):
    events = request.get('events', [])
    if not events:
        return {'dropout_probability': 0.5, 'risk_level': 'medium'}
    
    df = pd.DataFrame(events)
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    return analyzer.predict_dropout(df)


@app.post("/behavior/train")
def train_model():
    analyzer.train()
    analyzer.save()
    return {'ok': True, 'message': 'Model trained successfully'}
