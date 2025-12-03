from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.services.module_service import ModuleService
from app.schemas.module import ModuleCreate, ModuleUpdate


class ModuleController:

    @staticmethod
    def create(payload: ModuleCreate, db: Session):
        new_module = ModuleService.create(payload, db)
        return JSONResponse(
            content={
                "success": True,
                "message": "Module created successfully",
                "data": {
                    "id": new_module.id,
                    "name": new_module.name,
                    "description": new_module.description,
                    "status": new_module.status,
                },
            }
        )

    @staticmethod
    def list(db: Session):
        modules = ModuleService.list(db)
        return JSONResponse(
            content={
                "success": True,
                "message": "Modules retrieved successfully",
                "data": [
                    {
                        "id": m.id,
                        "name": m.name,
                        "description": m.description,
                        "status": m.status,
                    }
                    for m in modules
                ],
            }
        )

    @staticmethod
    def get_by_id(module_id: int, db: Session):
        module = ModuleService.get_by_id(module_id, db)
        if not module:
            return JSONResponse(
                content={
                    "success": False,
                    "message": f"Module with id {module_id} not found",
                },
                status_code=404,
            )
        return JSONResponse(
            content={
                "success": True,
                "message": "Module retrieved successfully",
                "data": {
                    "id": module.id,
                    "name": module.name,
                    "description": module.description,
                    "status": module.status,
                },
            }
        )

    @staticmethod
    def update(module_id: int, payload: ModuleUpdate, db: Session):
        module = ModuleService.update(module_id, payload, db)
        if not module:
            return JSONResponse(
                content={
                    "success": False,
                    "message": f"Module with id {module_id} not found",
                },
                status_code=404,
            )
        return JSONResponse(
            content={
                "success": True,
                "message": "Module updated successfully",
                "data": {
                    "id": module.id,
                    "name": module.name,
                    "description": module.description,
                    "status": module.status,
                },
            }
        )

    @staticmethod
    def delete(module_id: int, db: Session):
        deleted = ModuleService.delete(module_id, db)
        if not deleted:
            return JSONResponse(
                content={
                    "success": False,
                    "message": f"Module with id {module_id} not found",
                },
                status_code=404,
            )
        return JSONResponse(
            content={
                "success": True,
                "message": "Module deleted successfully",
            }
        )
