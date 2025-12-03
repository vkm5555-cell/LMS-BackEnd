from fastapi import APIRouter, Depends, Header, Path, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.db.session import db as database
from app.schemas.course_category import CourseCategoryCreate, CourseCategory, CourseCategoryUpdate
from app.controllers.course_category_controller import CourseCategoryController
from app.helper.dependencies import check_permission

router = APIRouter(prefix="/course-categories", tags=["Course Categories"])


@router.post("/", response_model=CourseCategory)
def create_course_category(
    payload: CourseCategoryCreate,
    authorization: str = Header(...),
    db: Session = Depends(database.get_db),
):
    has_permission = check_permission(authorization, "course_category", "create", db)
    if not has_permission:
        return JSONResponse(
            content={
                "error_code": 403,
                "success": False,
                "message": "Permission denied: Only admins can create users",
            },
            status_code=403,
        )
    return CourseCategoryController.create(payload, authorization, db)


@router.get("/", response_model=list[CourseCategory])
def list_course_categories(
    authorization: str = Header(...),
    page: int = Query(None, ge=1, description="Page number"),
    page_size: int = Query(None, le=100, description="Records per page"),
    skip: int = Query(None, ge=0, description="Number of records to skip"),
    limit: int = Query(None, le=100, description="Number of records to return"),
    search: str = Query(None, description="Search users by username or email"),
    db: Session = Depends(database.get_db),
):
    has_permission = check_permission(authorization, "course_category", "read", db)
    if not has_permission:
        return JSONResponse(
            content={
                "error_code": 403,
                "success": False,
                "message": "Permission denied: Only admins can create users",
            },
            status_code=403,
        )
    return CourseCategoryController.list(authorization, page, page_size, skip, limit, db, search=search)


@router.get("/{category_id}", response_model=CourseCategory)
def get_course_category(
    category_id: int = Path(...),
    authorization: str = Header(...),
    db: Session = Depends(database.get_db),
):
    return CourseCategoryController.get(category_id, authorization, db)



@router.get("/{category_id}", response_model=CourseCategory)
def get_course_category(
    category_id: int = Path(...),
    authorization: str = Header(...),
    db: Session = Depends(database.get_db),
):
    return CourseCategoryController.get(category_id, authorization, db)


@router.put("/{category_id}", response_model=CourseCategory)
def update_course_category(
    category_id: int = Path(...),
    payload: CourseCategoryUpdate = None,
    authorization: str = Header(...),
    db: Session = Depends(database.get_db),
):
    has_permission = check_permission(authorization, "course_category", "update", db)
    if not has_permission:
        return JSONResponse(
            content={
                "error_code": 403,
                "success": False,
                "message": "Permission denied: Only admins can create users",
            },
            status_code=403,
        )
    return CourseCategoryController.update(category_id, payload, authorization, db)


@router.delete("/{category_id}")
def delete_course_category(
    category_id: int = Path(...),
    authorization: str = Header(...),
    db: Session = Depends(database.get_db),
):
    has_permission = check_permission(authorization, "course_category", "delete", db)
    if not has_permission:
        return JSONResponse(
            content={
                "error_code": 403,
                "success": False,
                "message": "Permission denied: Only admins can create users",
            },
            status_code=403,
        )
    return CourseCategoryController.delete(category_id, authorization, db)
