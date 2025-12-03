# app/repositories/user_role_repo.py

from sqlalchemy.orm import Session
from app.models.models import UserRole

class UserRoleRepository:
    def create(self, db: Session, user_id: int, role: str) -> UserRole:
        user_role = UserRole(user_id=user_id, role=role)
        db.add(user_role)
        db.commit()
        db.refresh(user_role)
        return user_role
