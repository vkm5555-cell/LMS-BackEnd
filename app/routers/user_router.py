from fastapi import APIRouter, Depends, Header, Path, Query, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.controllers import user_controller
from app.db.session import db as database
from app.schemas.auth import UserCreate, UserUpdate, UserLogin, UserOut, Token, UpdateUserPermissionsRequest, AssignPermissionRequest
from app.schemas.user_details import UserDetailsBase
from app.controllers.user_controller import UserController
from app.helper.dependencies import check_permission
from app.models.models import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
def create_user(
    payload: UserCreate,
    db: Session = Depends(database.get_db),
    authorization: str = Header(...),
):

    try:
        has_permission = check_permission(authorization, "users", "create", db)
        if not has_permission:
            return JSONResponse(
                content={
                    "error_code": 403,
                    "success": False,
                    "message": "Permission denied: Only admins can create users",
                },
                status_code=403,
            )
        return UserController.create(payload, db, authorization)
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": str(e)},
            status_code=500,
        )

#Update User details
@router.post("/detail")
def assign_permissions(
        db: Session = Depends(database.get_db),
        authorization: str = Header(...),
        user_id: int = Form(...),
        name: str = Form(...),
        email: str = Form(...),
        mobile: str = Form(...),
        facebook: str = Form(""),
        xcom: str = Form(""),
        linkedin: str = Form(""),
        instagram: str = Form("")
):
    current_user = get_current_user(authorization, db)
    user_id = current_user["data"]["id"]

    payload = {
        "name": name,
        "email": email,
        "mobile": mobile,
        "facebook": facebook,
        "xcom": xcom,
        "linkedin": linkedin,
        "instagram": instagram
    }

    saved = UserController.save_or_update_user_details(
        db=db,
        user_id=user_id,
        payload=payload
    )

    return {
        "success": True,
        "message": "User details saved successfully",
        "data": saved
    }

@router.get("/")
def list_users(
    authorization: str = Header(...),
    db: Session = Depends(database.get_db),
    page: int = Query(None, ge=1, description="Page number"),
    page_size: int = Query(None, le=100, description="Records per page"),
    skip: int = Query(None, ge=0, description="Number of records to skip"),
    limit: int = Query(None, le=100, description="Number of records to return"),
    search: str = Query(None, description="Search users by username or email"),
):
    has_permission = check_permission(authorization, "users", "read", db)
    if not has_permission:
        return JSONResponse(
            content={
                "error_code": 403,
                "success": False,
                "message": "Permission denied: You are not authorized to view users",
            },
            status_code=403,
        )

    # Pagination logic
    if page is not None and page_size is not None:
        skip = (page - 1) * page_size
        limit = page_size
    elif skip is None or limit is None:
        skip, limit = 0, 10  # default

    # Build query
    query = db.query(User)

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                User.username.ilike(search_pattern),
                User.email.ilike(search_pattern)
            )
        )

    total = query.count()
    users = query.offset(skip).limit(limit).all()

    return UserController.list(db, skip=skip, limit=limit, users=users, total=total)

#Get user detail by the user token
@router.get("/user-details-by-token")
def get_user_detail_by_token(
    authorization: str = Header(None),
    db: Session = Depends(database.get_db)
):
    if not authorization:
        return JSONResponse(
            content={"success": False, "message": "Authorization header missing"},
            status_code=400
        )

    try:
        user = UserController.get_user_by_token(authorization, db)
        if not user:
            return JSONResponse(
                content={"success": False, "message": "Invalid or expired token"},
                status_code=401
            )
        return {"success": True, "data": user}
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": str(e)},
            status_code=500
        )

@router.put("/{user_id}")
def update_user(
    user_id: int = Path(...),
    payload: UserUpdate = None,
    db: Session = Depends(database.get_db),
    authorization: str = Header(...),
):
    #return user_id
    has_permission = check_permission(authorization, "users", "update", db)
    if not has_permission:
        return JSONResponse(
            content={
                "error_code": 403,
                "success": False,
                "message": "Permission denied: You are not authorized to update users",
            },
            status_code=403,
        )
    return UserController.update(user_id, payload, db)


@router.delete("/{user_id}")
def delete_user(
    user_id: int = Path(...),
    db: Session = Depends(database.get_db),
    authorization: str = Header(...),
):
    has_permission = check_permission(authorization, "users", "delete", db)
    if not has_permission:
        return JSONResponse(
            content={
                "error_code": 403,
                "success": False,
                "message": "Permission denied: You are not authorized to delete users",
            },
            status_code=403,
        )
    return UserController.delete(user_id, db)


@router.get("/{user_id}")
def get_user(
    user_id: int = Path(...),
    db: Session = Depends(database.get_db),
    authorization: str = Header(...),
):
    return user_id
    has_permission = check_permission(authorization, "users", "read", db)
    if not has_permission:
        return JSONResponse(
            content={
                "error_code": 403,
                "success": False,
                "message": "Permission denied: You are not authorized to view users",
            },
            status_code=403,
        )
    #return user_id
    return UserController.get_by_id(user_id, db)


@router.get("/getUser/{user_id}")
def get_user_by_id(
    user_id: int = Path(...),
    db: Session = Depends(database.get_db),
    authorization: str = Header(...),
):
    #return user_id
    has_permission = check_permission(authorization, "users", "read", db)
    if not has_permission:
        return JSONResponse(
            content={
                "error_code": 403,
                "success": False,
                "message": "Permission denied: You are not authorized to view users",
            },
            status_code=403,
        )
    #return user_id
    return UserController.get_user_with_permissions(user_id, db)


@router.get("/{user_id}/permissions")
def get_user_permissions_route(user_id: int, db: Session = Depends(database.get_db), authorization: str = Header(...),):
    has_permission = check_permission(authorization, "users", "read", db)
    if not has_permission:
        return JSONResponse(
            content={
                "error_code": 403,
                "success": False,
                "message": "Permission denied: You are not authorized to view users",
            },
            status_code=403,
        )
    return UserController.get_permissions(user_id, db)

@router.get("/permissions/{permission_id}")
def get_permission_route(permission_id: int, db: Session = Depends(database.get_db)):
    return UserController.get_permission(permission_id, db)

@router.put("/{permissions_id}/permissions")
def update_user_permissions_route(
    permissions_id: int,
    payload: UpdateUserPermissionsRequest,
    db: Session = Depends(database.get_db),
    authorization: str = Header(...),
):
    has_permission = check_permission(authorization, "users", "update", db)
    if not has_permission:
        return JSONResponse(
            content={
                "error_code": 403,
                "success": False,
                "message": "Permission denied: You are not authorized to update user permissions",
            },
            status_code=403,
        )

    return UserController.update_permissions(permissions_id, payload.permission_ids, db)


@router.get("/{user_id}/roles")
def get_user_roles(
        user_id: int = Path(...),
        db: Session = Depends(database.get_db),
        authorization: str = Header(...),
):
    has_permission = check_permission(authorization, "users", "read", db)
    if not has_permission:
        return JSONResponse(
            content={
                "error_code": 403,
                "success": False,
                "message": "Permission denied: You are not authorized to view user roles",
            },
            status_code=403,
        )

    return UserController.get_user_roles(user_id, db)


@router.post("/assign-module-permissions")
def assign_permissions(
        payload: AssignPermissionRequest,
        db: Session = Depends(database.get_db),
        authorization: str = Header(...),
):
    #return payload
    has_permission = check_permission(authorization, "permissions", "create", db)
    if not has_permission:
        return JSONResponse(
            content={
                "error_code": 403,
                "success": False,
                "message": "Permission denied: You are not authorized to assign permissions",
            },
            status_code=403,
        )

    return UserController.assign_permissions(payload, db)


@router.post("/me")
def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(database.get_db)
):
    if not authorization:
        return JSONResponse(
            content={"success": False, "message": "Authorization header missing"},
            status_code=400
        )

    try:
        user = UserController.get_user_by_token(authorization, db)
        if not user:
            return JSONResponse(
                content={"success": False, "message": "Invalid or expired token"},
                status_code=401
            )
        return {"success": True, "data": user}
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": str(e)},
            status_code=500
        )

# Get student users
@router.get("/students/by-role/{role_name}")
def get_users_by_role(role_name: str, db: Session = Depends(database.get_db)):
    return UserController.get_users_by_role(role_name, db)








