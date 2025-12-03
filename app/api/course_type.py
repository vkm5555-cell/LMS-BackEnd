from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import db as database
from app.schemas.course_type import CourseTypeCreate, CourseTypeOut
from app.services.course_type_service import CourseTypeService
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/course-types", tags=["Course Types"])
service = CourseTypeService()

@router.post("/", response_model=CourseTypeOut)
def create_course_type(
    payload: CourseTypeCreate,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user),
):
    if current_user.role not in ["admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    return service.create(db, payload)

@router.get("/", response_model=list[CourseTypeOut])
def list_course_types(
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(get_current_user),
):
    return service.list(db)
