from fastapi import APIRouter, Depends, Header, Path
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.db.session import db as database
from app.schemas.course_type import CourseTypeCreate, CourseTypeOut
from app.services.course_type_service import CourseTypeService
from app.models.models import User
from app.models.course_type import CourseType
from app.helper.dependencies import check_permission

router = APIRouter(prefix="/course-types", tags=["Course Types"])
service = CourseTypeService()

# ---------------- Helper Function ---------------- #
def validate_user_token(authorization: str, db: Session):
    """Validate token, expiry, and return user"""
    if not authorization.startswith("Bearer "):
        return None, JSONResponse(
            status_code=401,
            content={"error_code": 300, "success": False, "message": "Invalid authorization header format"}
        )

    token = authorization.split(" ")[1]
    user = db.query(User).filter(User.access_token == token).first()
    if not user:
        return None, JSONResponse(
            status_code=401,
            content={"error_code": 300, "success": False, "message": "Invalid token"}
        )

    expiry = user.token_expiry
    if expiry.tzinfo is None:
        expiry = expiry.replace(tzinfo=timezone.utc)
    if expiry < datetime.now(timezone.utc):
        return None, JSONResponse(
            status_code=401,
            content={"error_code": 300, "success": False, "message": "Token expired"}
        )

    return user, None


# ---------------- CREATE ---------------- #
@router.post("/", response_model=CourseTypeOut)
def create_course_type(
    payload: CourseTypeCreate,
    authorization: str = Header(...),
    db: Session = Depends(database.get_db),
):
    user, error_response = validate_user_token(authorization, db)
    if error_response:
        return error_response

    has_permission = check_permission(authorization, "course_types", "create", db)
    if not has_permission:
        return JSONResponse(
            content={
                "error_code": 403,
                "success": False,
                "message": "Permission denied: You do not have permission to perform this action.",
            },
            status_code=403,
        )

    existing = db.query(CourseType).filter(CourseType.name == payload.name).first()
    if existing:
        return JSONResponse(
            status_code=400,
            content={"error_code": 301, "success": False, "message": f"Course type '{payload.name}' already exists"}
        )

    new_course_type = service.create(db, payload)
    return JSONResponse(
        status_code=201,
        content={
            "success": True,
            "message": "Course type created successfully",
            "data": CourseTypeOut.from_orm(new_course_type).dict(),
        },
    )


# ---------------- LIST ---------------- #
@router.get("/", response_model=list[CourseTypeOut])
def list_course_types(
    authorization: str = Header(...),
    db: Session = Depends(database.get_db),
    
):
    has_permission = check_permission(authorization, "course_types", "read", db)
    if not has_permission:
        return JSONResponse(
            content={
                "error_code": 403,
                "success": False,
                "message": "Permission denied: You do not have permission to perform this action.",
            },
            status_code=403,
        )
    user, error_response = validate_user_token(authorization, db)
    if error_response:
        return error_response

    course_types = service.list(db)
    course_types = sorted(course_types, key=lambda ct: ct.id, reverse=True)

    return JSONResponse(
        status_code=200,
        content={
            "error_code": 301,
            "success": True,
            "message": "Course types fetched successfully",
            "data": [CourseTypeOut.from_orm(ct).dict() for ct in course_types],
        },
    )


# ---------------- UPDATE ---------------- #
@router.put("/{course_type_id}", response_model=CourseTypeOut)
def update_course_type(
    course_type_id: int = Path(..., description="ID of the course type to update"),
    payload: CourseTypeCreate = None,
    authorization: str = Header(...),
    db: Session = Depends(database.get_db),
):
    user, error_response = validate_user_token(authorization, db)
    if error_response:
        return error_response

    if payload.role != user.role:
        return JSONResponse(
            status_code=403,
            content={"error_code": 300, "success": False, "message": "Role mismatch. Not authorized"},
        )

    course_type = db.query(CourseType).filter(CourseType.id == course_type_id).first()
    if not course_type:
        return JSONResponse(
            status_code=404,
            content={"error_code": 302, "success": False, "message": "Course type not found"},
        )

    # Check for duplicate name (excluding current record)
    existing = db.query(CourseType).filter(
        CourseType.name == payload.name, CourseType.id != course_type_id
    ).first()
    if existing:
        return JSONResponse(
            status_code=400,
            content={"error_code": 301, "success": False, "message": f"Course type '{payload.name}' already exists"},
        )

    course_type.name = payload.name
    course_type.description = payload.description
    course_type.status = payload.status
    db.commit()
    db.refresh(course_type)

    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": "Course type updated successfully",
            "data": CourseTypeOut.from_orm(course_type).dict(),
        },
    )


# ---------------- DELETE ---------------- #
@router.delete("/{course_type_id}")
def delete_course_type(
    course_type_id: int = Path(..., description="ID of the course type to delete"),
    authorization: str = Header(...),
    db: Session = Depends(database.get_db),
):
    user, error_response = validate_user_token(authorization, db)
    if error_response:
        return error_response

    course_type = db.query(CourseType).filter(CourseType.id == course_type_id).first()
    if not course_type:
        return JSONResponse(
            status_code=404,
            content={"error_code": 302, "success": False, "message": "Course type not found"},
        )

    db.delete(course_type)
    db.commit()

    return JSONResponse(
        status_code=200,
        content={"success": True, "message": "Course type deleted successfully"},
    )

# ---------------- GET BY ID ---------------- #
@router.get("/{course_type_id}", response_model=CourseTypeOut)
def get_course_type(
    course_type_id: int = Path(..., description="ID of the course type to fetch"),
    authorization: str = Header(...),
    db: Session = Depends(database.get_db),
):
    user, error_response = validate_user_token(authorization, db)
    if error_response:
        return error_response

    course_type = db.query(CourseType).filter(CourseType.id == course_type_id).first()
    if not course_type:
        return JSONResponse(
            status_code=404,
            content={"error_code": 302, "success": False, "message": "Course type not found"},
        )

    return JSONResponse(
        status_code=200,
        content={
            "error_code": 301,
            "success": True,
            "message": "Course type fetched successfully",
            "data": CourseTypeOut.from_orm(course_type).dict(),
        },
    )
    
