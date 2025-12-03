from fastapi import APIRouter, Depends, Header, Path
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.session import db as database
from app.schemas.module import ModuleCreate, ModuleUpdate
from app.controllers.module_controller import ModuleController
from app.helper.dependencies import check_permission

router = APIRouter(prefix="/modules", tags=["Modules"])


@router.post("/")
def create_module(
    payload: ModuleCreate,
    db: Session = Depends(database.get_db),
    authorization: str = Header(...),
):
    has_permission = check_permission(authorization, "modules", "create", db)
    if not has_permission:
        return JSONResponse(
            content={
                "error_code": 401,
                "success": False,
                "message": "Permission denied: You are not authorized to view modules",
            },
        )
    return ModuleController.create(payload, db)


@router.get("/")
def list_modules(
    authorization: str = Header(...),
    db: Session = Depends(database.get_db),
):
    has_permission = check_permission(authorization, "modules", "read", db)

    if not has_permission:
        return JSONResponse(
            content={
                "error_code": 401,
                "success": False,
                "message": "Permission denied: You are not authorized to view modules",
            },
        )

    return ModuleController.list(db)


@router.put("/{module_id}")
def update_module(
    module_id: int = Path(...),
    payload: ModuleUpdate = None,
    db: Session = Depends(database.get_db),
    authorization: str = Header(...),
):
    has_permission = check_permission(authorization, "modules", "update", db)
    if not has_permission:
        return JSONResponse(
            content={
                "error_code": 401,
                "success": False,
                "message": "Permission denied: You are not authorized to update modules",
            },
        )
    return ModuleController.update(module_id, payload, db)


@router.delete("/{module_id}")
def delete_module(
    module_id: int = Path(...),
    db: Session = Depends(database.get_db),
    authorization: str = Header(...),
):

    has_permission = check_permission(authorization, "modules", "delete", db)
    if not has_permission:
        return JSONResponse(
            content={
                "error_code": 401,
                "success": False,
                "message": "Permission denied: You are not authorized to delete modules",
            },
        )
    return ModuleController.delete(module_id, db)


@router.get("/{module_id}")
def get_module(
    module_id: int = Path(...),
    db: Session = Depends(database.get_db),
    authorization: str = Header(...),
):
    has_permission = check_permission(authorization, "modules", "update", db)
    if not has_permission:
        return JSONResponse(
            content={
                "error_code": 401,
                "success": False,
                "message": "Permission denied: You are not authorized to view modules",
            },
        )
    return ModuleController.get_by_id(module_id, db)
