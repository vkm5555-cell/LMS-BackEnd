# app/services/module_service.py

from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.models import Module
from app.schemas.module import ModuleCreate, ModuleUpdate


class ModuleService:

    @staticmethod
    def create(payload: ModuleCreate, db: Session) -> Module:
        new_module = Module(
            name=payload.name,
            description=payload.description,
            status="active",
        )
        db.add(new_module)
        db.commit()
        db.refresh(new_module)
        return new_module

    @staticmethod
    def list(db: Session) -> list[Module]:
        return db.query(Module).order_by(desc(Module.id)).all()

    @staticmethod
    def get_by_id(module_id: int, db: Session) -> Module | None:
        return db.query(Module).filter(Module.id == module_id).first()

    @staticmethod
    def update(module_id: int, payload: ModuleUpdate, db: Session) -> Module | None:
        module = db.query(Module).filter(Module.id == module_id).first()
        if not module:
            return None

        if payload.name is not None:
            module.name = payload.name
        if payload.description is not None:
            module.description = payload.description

        db.commit()
        db.refresh(module)
        return module

    @staticmethod
    def delete(module_id: int, db: Session) -> bool:
        module = db.query(Module).filter(Module.id == module_id).first()
        if not module:
            return False

        db.delete(module)
        db.commit()
        return True
