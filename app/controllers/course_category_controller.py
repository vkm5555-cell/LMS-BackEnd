from fastapi.responses import JSONResponse
from fastapi import Header, Path, Query
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from sqlalchemy import or_
from app.models.models import User
from app.models.course_category import CourseCategory
from app.models.course_category import CourseCategory as CourseCategoryModel
from app.schemas.course_category import CourseCategoryCreate, CourseCategory, CourseCategoryUpdate
from app.services import course_category_service
from app.helper.dependencies import check_permission


class CourseCategoryController:

    @staticmethod
    def validate_user_token(authorization: str, db: Session):
        """Validate token, expiry, and return user or error response"""
        if not authorization.startswith("Bearer "):
            return None, JSONResponse(
                status_code=401,
                content={"error_code": 300, "success": False, "message": "Invalid authorization header format"},
            )

        token = authorization.split(" ")[1]
        user = db.query(User).filter(User.access_token == token).first()
        if not user:
            return None, JSONResponse(
                status_code=401,
                content={"error_code": 300, "success": False, "message": "Invalid token"},
            )

        expiry = user.token_expiry
        if expiry.tzinfo is None:
            expiry = expiry.replace(tzinfo=timezone.utc)
        if expiry < datetime.now(timezone.utc):
            return None, JSONResponse(
                status_code=401,
                content={"error_code": 300, "success": False, "message": "Token expired"},
            )

        return user, None

    # ---------------- CREATE ---------------- #
    @staticmethod
    def create(payload: CourseCategoryCreate, authorization: str, db: Session):
        has_permission = check_permission(authorization, "course_category", "create", db)
        if not has_permission:
            return JSONResponse(
                content={
                    "error_code": 403,
                    "success": False,
                    "message": "Permission denied: You are not authorized to create course categories",
                },
                status_code=403,
            )

        existing = db.query(CourseCategoryModel).filter(CourseCategoryModel.name == payload.name).first()
        if existing:
            return JSONResponse(
                status_code=400,
                content={"error_code": 301, "success": False, "message": f"Category '{payload.name}' already exists"},
            )

        new_category = course_category_service.create_category(db, payload)
        return new_category

    # ---------------- LIST ---------------- #
    @staticmethod
    def list(authorization: str, page, page_size, skip: int, limit: int, db: Session, search):
        user, error_response = CourseCategoryController.validate_user_token(authorization, db)
        if error_response:
            return error_response

            # Pagination logic
        if page is not None and page_size is not None:
            skip = (page - 1) * page_size
            limit = page_size
        elif skip is None or limit is None:
            skip, limit = 0, 10  # default

        result = course_category_service.get_categories(db, skip=skip, limit=limit, search=search)

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Course categories fetched successfully",
                "total": result["total"],
                "skip": result["skip"],
                "limit": result["limit"],
                "data": [CourseCategory.from_orm(c).dict() for c in result["items"]],
            },
        )

    # ---------------- GET BY ID ---------------- #
    @staticmethod
    def get(category_id: int, authorization: str, db: Session):
        user, error_response = CourseCategoryController.validate_user_token(authorization, db)
        if error_response:
            return error_response

        category = course_category_service.get_category(db, category_id)
        if not category:
            return JSONResponse(
                status_code=404,
                content={"error_code": 302, "success": False, "message": "Course category not found"},
            )

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Course category fetched successfully",
                "data": CourseCategory.from_orm(category).dict(),
            },
        )

    # ---------------- UPDATE ---------------- #
    @staticmethod
    def update(category_id: int, payload: CourseCategoryUpdate, authorization: str, db: Session):
        user, error_response = CourseCategoryController.validate_user_token(authorization, db)
        if error_response:
            return error_response

        category = db.query(CourseCategoryModel).filter(CourseCategoryModel.id == category_id).first()
        if not category:
            return JSONResponse(
                status_code=404,
                content={"error_code": 302, "success": False, "message": "Course category not found"},
            )

        if payload.name:
            existing = db.query(CourseCategoryModel).filter(
                CourseCategoryModel.name == payload.name, CourseCategoryModel.id != category_id
            ).first()
            if existing:
                return JSONResponse(
                    status_code=400,
                    content={"error_code": 301, "success": False, "message": f"Category '{payload.name}' already exists"},
                )

        updated = course_category_service.update_category(db, category_id, payload)
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Course category updated successfully",
                "data": CourseCategory.from_orm(updated).dict(),
            },
        )

    # ---------------- DELETE ---------------- #
    @staticmethod
    def delete(category_id: int, authorization: str, db: Session):
        user, error_response = CourseCategoryController.validate_user_token(authorization, db)
        if error_response:
            return error_response

        category = course_category_service.get_category(db, category_id)
        if not category:
            return JSONResponse(
                status_code=404,
                content={"error_code": 302, "success": False, "message": "Course category not found"},
            )

        course_category_service.delete_category(db, category_id)
        return JSONResponse(
            status_code=200,
            content={"success": True, "message": "Course category deleted successfully"},
        )
