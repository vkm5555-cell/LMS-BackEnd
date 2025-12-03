from sqlalchemy.orm import Session
from app.models.models import ActivityLog

class ActivityRepository:
    def create(self, db: Session, user_id: int, action: str):
        log = ActivityLog(user_id=user_id, action=action)
        db.add(log)
        db.commit()
        db.refresh(log)
        return log