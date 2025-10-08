from celery import Celery
from .config import settings
import time
from sqlalchemy.orm import Session
from .models import Notification
from .db import SessionLocal

celery = Celery("workers", broker=settings.REDIS_URL, backend=settings.REDIS_URL)

@celery.task(bind=True, max_retries=3)
def send_email_task(self, notification_id: int):
    # Placeholder - integrate with real mailer
    db: Session = SessionLocal()
    try:
        notif = db.query(Notification).filter(Notification.id == notification_id).first()
        if not notif:
            return {"error": "not found"}

        # Simulate sending email (replace with SendGrid/SES etc.)
        print(f"[EMAIL] Sending to user {notif.user_id}: {notif.title} - {notif.body}")
        # update delivered flag - in real system you'd only mark delivered after success/ack
        notif.delivered = True
        db.commit()
        return {"ok": True}
    except Exception as exc:
        self.retry(exc=exc, countdown=10)
    finally:
        db.close()

@celery.task
def send_push_notification_task(notification_id: int):
    # Placeholder for FCM/APNs integration
    db = SessionLocal()
    try:
        notif = db.query(Notification).filter(Notification.id == notification_id).first()
        if not notif:
            return {"error": "not found"}
        print(f"[PUSH] Would push to user {notif.user_id}: {notif.title}")
        notif.delivered = True
        db.commit()
        return {"ok": True}
    finally:
        db.close()
