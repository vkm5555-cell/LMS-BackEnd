from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.models import Role
from app.schemas.role import RoleCreate, RoleUpdate

class RoleService:
    def create(self, db: Session, payload: RoleCreate) -> Role:
        role = Role(name=payload.name, description=payload.description)
        db.add(role)
        db.commit()
        db.refresh(role)
        return role

    def list(self, db: Session) -> list[Role]:
        return db.query(Role).order_by(desc(Role.id)).all()

    def update(self, db: Session, role_id: int, payload: RoleUpdate) -> Role | None:
        role = db.query(Role).filter(Role.id == role_id).first()
        if role:
            role.name = payload.name
            role.description = payload.description
            db.commit()
            db.refresh(role)
        return role

    def delete(self, db: Session, role_id: int) -> bool:
        role = db.query(Role).filter(Role.id == role_id).first()
        if role:
            db.delete(role)
            db.commit()
            return True
        return False

    def get_by_id(self, db: Session, role_id: int) -> Role | None:
        return db.query(Role).filter(Role.id == role_id).first()
