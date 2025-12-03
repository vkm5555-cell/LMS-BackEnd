from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.schemas.role import RoleCreate, RoleUpdate, RoleOut
from app.services.role_service import RoleService
from app.models.models import Role

service = RoleService()

class RoleController:
    @staticmethod
    def create(payload: RoleCreate, db: Session):
        existing = db.query(Role).filter(Role.name == payload.name).first()
        if existing:
            return JSONResponse(
                status_code=301,
                content={"error_code": 301, "success": False, "message": f"Role '{payload.name}' already exists"},
            )
        role = service.create(db, payload)
        return JSONResponse(
            status_code=201,
            content={"success": True, "message": "Role created", "data": RoleOut.from_orm(role).dict()},
        )

    @staticmethod
    def list(db: Session):
        roles = service.list(db)
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Roles fetched",
                "data": [RoleOut.from_orm(r).dict() for r in roles],
            },
        )

    @staticmethod
    def update(role_id: int, payload: RoleUpdate, db: Session):
        role = service.update(db, role_id, payload)
        if not role:
            return JSONResponse(status_code=404, content={"success": False, "message": "Role not found"})
        return JSONResponse(
            status_code=200,
            content={"success": True, "message": "Role updated", "data": RoleOut.from_orm(role).dict()},
        )

    @staticmethod
    def delete(role_id: int, db: Session):
        deleted = service.delete(db, role_id)
        if not deleted:
            return JSONResponse(status_code=404, content={"success": False, "message": "Role not found"})
        return JSONResponse(status_code=200, content={"success": True, "message": "Role deleted"})

    @staticmethod
    def get_by_id(role_id: int, db: Session):
        role = service.get_by_id(db, role_id)
        if not role:
            return JSONResponse(status_code=404, content={"success": False, "message": "Role not found"})
        return JSONResponse(
            status_code=200,
            content={"success": True, "message": "Role fetched", "data": RoleOut.from_orm(role).dict()},
        )
