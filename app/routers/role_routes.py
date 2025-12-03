from fastapi import APIRouter, Depends, Header, Path
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.session import db as database
from app.schemas.role import RoleCreate, RoleUpdate
from app.controllers.role_controller import RoleController
from app.helper.dependencies import check_permission

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/")
def create_role(payload: RoleCreate, db: Session = Depends(database.get_db), authorization: str = Header(...)):
    has_permission = check_permission(authorization, "roles", "read", db)
    if not has_permission:
        return JSONResponse(
            content={
                "error_code": 401,
                "success": False,
                "message": "Permission denied: You are not authorized to view roles",
            },
        )
    return RoleController.create(payload, db)

@router.get("/")
def list_roles(authorization: str = Header(...), db: Session = Depends(database.get_db)):
    check_permission(authorization, "roles", "read", db)
    has_permission = check_permission(authorization, "roles", "read", db)
    if not has_permission:
        return JSONResponse(
            content={
                "error_code": 401,
                "success": False,
                "message": "Permission denied: You are not authorized to view roles",
            },
        )

    return RoleController.list(db)

@router.put("/{role_id}")
def update_role(role_id: int = Path(...), payload: RoleUpdate = None, db: Session = Depends(database.get_db), authorization: str = Header(...)):
    has_permission = check_permission(authorization, "roles", "read", db)
    if not has_permission:
        return JSONResponse(
             content={
                "error_code": 401,
                "success": False,
                "message": "Permission denied: You are not authorized to view roles",
            },
        )
    return RoleController.update(role_id, payload, db)


@router.delete("/{role_id}")
def delete_role(role_id: int = Path(...), db: Session = Depends(database.get_db), authorization: str = Header(...)):
    check_permission(authorization, "roles", "delete", db)
    has_permission = check_permission(authorization, "roles", "read", db)
    if not has_permission:
        return JSONResponse(
            content={
                "error_code": 401,
                "success": False,
                "message": "Permission denied: You are not authorized to view roles",
            },
        )
    return RoleController.delete(role_id, db)

@router.get("/{role_id}")
def get_role(role_id: int = Path(...), db: Session = Depends(database.get_db), authorization: str = Header(...)):
    check_permission(authorization, "roles", "read", db)
    has_permission = check_permission(authorization, "roles", "read", db)
    if not has_permission:
        return JSONResponse(
            content={
                "error_code": 401,
                "success": False,
                "message": "Permission denied: You are not authorized to view roles",
            },
        )
    return RoleController.get_by_id(role_id, db)
