from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .. import schemas, models
from ..db import get_db

router = APIRouter(prefix="/streak", tags=["streak"])


@router.get("/{user_id}", response_model=schemas.StreakOut)
def get_streak(user_id: int, db: Session = Depends(get_db)):
    streak = db.query(models.UserStreak).filter(models.UserStreak.user_id == user_id).first()
    if not streak:
        streak = models.UserStreak(
            user_id=user_id,
            current_streak=0,
            longest_streak=0,
            freeze_count=0,
            total_active_days=0
        )
        db.add(streak)
        db.commit()
        db.refresh(streak)
    return streak


@router.post("/activity", response_model=schemas.StreakActivityOut)
def log_activity(payload: schemas.StreakActivityCreate, db: Session = Depends(get_db)):
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    streak = db.query(models.UserStreak).filter(models.UserStreak.user_id == payload.user_id).first()
    if not streak:
        streak = models.UserStreak(user_id=payload.user_id)
        db.add(streak)
    
    activity = models.StreakActivity(
        user_id=payload.user_id,
        minutes_active=payload.minutes_active,
        sessions_completed=payload.sessions_completed,
        content_type=payload.content_type,
        activity_date=today
    )
    
    if streak.last_activity_date:
        last_date = streak.last_activity_date.replace(hour=0, minute=0, second=0, microsecond=0)
        days_diff = (today - last_date).days
        
        if days_diff == 0:
            activity.streak_continued = True
            streak.current_streak += 1
        elif days_diff == 1:
            activity.streak_continued = True
            streak.current_streak += 1
            if not streak.streak_start_date:
                streak.streak_start_date = today - timedelta(days=days_diff - 1)
        else:
            activity.streak_continued = False
            streak.current_streak = 1
            streak.streak_start_date = today
    else:
        streak.current_streak = 1
        streak.streak_start_date = today
        activity.streak_continued = True
    
    if streak.current_streak > streak.longest_streak:
        streak.longest_streak = streak.current_streak
    
    streak.last_activity_date = today
    streak.total_active_days += 1
    streak.updated_at = datetime.utcnow()
    
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity


@router.post("/{user_id}/use-freeze")
def use_freeze(user_id: int, db: Session = Depends(get_db)):
    streak = db.query(models.UserStreak).filter(models.UserStreak.user_id == user_id).first()
    if not streak:
        raise HTTPException(status_code=404, detail="streak not found")
    
    if streak.freeze_count <= 0:
        raise HTTPException(status_code=400, detail="no freezes available")
    
    streak.freeze_count -= 1
    streak.updated_at = datetime.utcnow()
    db.commit()
    return {"ok": True, "freeze_count": streak.freeze_count}


@router.get("/{user_id}/history", response_model=list[schemas.StreakActivityOut])
def get_streak_history(user_id: int, limit: int = 30, db: Session = Depends(get_db)):
    activities = db.query(models.StreakActivity).filter(
        models.StreakActivity.user_id == user_id
    ).order_by(models.StreakActivity.activity_date.desc()).limit(limit).all()
    return activities
