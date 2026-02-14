from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models
from ..db import get_db

router = APIRouter()

@router.post("/", response_model=schemas.ActionOut)
def create_action(payload: schemas.ActionCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    action = models.Action(user_id=payload.user_id, type=payload.type, payload=payload.payload)
    db.add(action)
    db.commit()
    db.refresh(action)
    return action

@router.get("/", response_model=list[schemas.ActionOut])
def list_actions(user_id: int, limit: int = 50, db: Session = Depends(get_db)):
    actions = db.query(models.Action).filter(models.Action.user_id == user_id).order_by(models.Action.created_at.desc()).limit(limit).all()
    return actions
