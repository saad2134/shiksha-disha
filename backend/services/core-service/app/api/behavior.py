from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from datetime import datetime
from .. import schemas, models
from ..db import get_db

router = APIRouter()


@router.post("/session/start", response_model=schemas.SessionOut)
def start_session(payload: schemas.SessionStart, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    
    session = models.LearningSession(
        user_id=payload.user_id,
        content_id=payload.content_id,
        content_type=payload.content_type,
        started_at=datetime.utcnow()
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@router.post("/session/end", response_model=schemas.SessionOut)
def end_session(payload: schemas.SessionEnd, db: Session = Depends(get_db)):
    session = db.query(models.LearningSession).filter(models.LearningSession.id == payload.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="session not found")
    
    session.ended_at = datetime.utcnow()
    session.duration_seconds = payload.duration_seconds
    if payload.engagement_score is not None:
        session.engagement_score = payload.engagement_score
    
    db.commit()
    db.refresh(session)
    return session


@router.get("/session/{session_id}", response_model=schemas.SessionOut)
def get_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(models.LearningSession).filter(models.LearningSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="session not found")
    return session


@router.post("/event", response_model=schemas.BehaviorEventOut)
def log_event(payload: schemas.BehaviorEventCreate, db: Session = Depends(get_db)):
    event = models.BehaviorEvent(
        user_id=payload.user_id,
        session_id=payload.session_id,
        event_type=payload.event_type,
        content_id=payload.content_id,
        content_type=payload.content_type,
        meta=payload.meta,
        timestamp=datetime.utcnow()
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@router.get("/events/{user_id}", response_model=list[schemas.BehaviorEventOut])
def get_user_events(user_id: int, limit: int = 100, session_id: int = None, db: Session = Depends(get_db)):
    query = db.query(models.BehaviorEvent).filter(models.BehaviorEvent.user_id == user_id)
    if session_id:
        query = query.filter(models.BehaviorEvent.session_id == session_id)
    events = query.order_by(models.BehaviorEvent.timestamp.desc()).limit(limit).all()
    return events


@router.get("/profile/{user_id}", response_model=schemas.EngagementProfileOut)
def get_engagement_profile(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(models.UserEngagementProfile).filter(models.UserEngagementProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="profile not found")
    return profile


@router.post("/profile/{user_id}/update")
def update_engagement_profile(
    user_id: int,
    avg_engagement_score: float = 0.0,
    preferred_content_type: str = None,
    preferred_difficulty: str = None,
    dropout_risk_score: float = 0.0,
    db: Session = Depends(get_db)
):
    profile = db.query(models.UserEngagementProfile).filter(models.UserEngagementProfile.user_id == user_id).first()
    
    if not profile:
        profile = models.UserEngagementProfile(
            user_id=user_id,
            avg_engagement_score=avg_engagement_score,
            preferred_content_type=preferred_content_type,
            preferred_difficulty=preferred_difficulty,
            dropout_risk_score=dropout_risk_score,
            last_updated=datetime.utcnow()
        )
        db.add(profile)
    else:
        profile.avg_engagement_score = avg_engagement_score
        profile.preferred_content_type = preferred_content_type
        profile.preferred_difficulty = preferred_difficulty
        profile.dropout_risk_score = dropout_risk_score
        profile.last_updated = datetime.utcnow()
    
    db.commit()
    return {"ok": True, "user_id": user_id}


@router.get("/sessions/{user_id}", response_model=list[schemas.SessionOut])
def get_user_sessions(user_id: int, limit: int = 20, db: Session = Depends(get_db)):
    sessions = db.query(models.LearningSession).filter(
        models.LearningSession.user_id == user_id
    ).order_by(models.LearningSession.started_at.desc()).limit(limit).all()
    return sessions
