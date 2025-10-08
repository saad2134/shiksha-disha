from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, WebSocket
from sqlalchemy.orm import Session
from .. import schemas, models, workers
from ..db import get_db
from ..realtime import manager

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.post("/send", response_model=schemas.NotificationOut)
def send_notification(payload: schemas.NotificationCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    notif = models.Notification(
        user_id=payload.user_id,
        title=payload.title,
        body=payload.body,
        metadata=payload.metadata or {}
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)

    # Real-time deliver via WebSocket if connected
    import asyncio
    try:
        asyncio.create_task(manager.send_personal(payload.user_id, {
            "id": notif.id,
            "title": notif.title,
            "body": notif.body,
            "metadata": notif.metadata,
            "created_at": str(notif.created_at)
        }))
    except Exception:
        pass

    # Dispatch async tasks to send email/push (Celery)
    if payload.deliver_immediately:
        workers.send_email_task.delay(notif.id)
        workers.send_push_notification_task.delay(notif.id)

    return notif

@router.get("/", response_model=list[schemas.NotificationOut])
def list_notifications(user_id: int, unread_only: bool = False, db: Session = Depends(get_db)):
    q = db.query(models.Notification).filter(models.Notification.user_id == user_id)
    if unread_only:
        q = q.filter(models.Notification.read == False)
    return q.order_by(models.Notification.created_at.desc()).limit(100).all()

@router.post("/{notif_id}/mark_read", response_model=schemas.NotificationOut)
def mark_read(notif_id: int, db: Session = Depends(get_db)):
    notif = db.query(models.Notification).filter(models.Notification.id == notif_id).first()
    if not notif:
        raise HTTPException(status_code=404, detail="notification not found")
    notif.read = True
    db.commit()
    db.refresh(notif)
    return notif
