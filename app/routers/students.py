from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import db as database
from app.schemas.student import StudentCreate, StudentOut
from app.services.student_service import StudentService

router = APIRouter(prefix="/students", tags=["Students"])
service = StudentService()

@router.post("", response_model=StudentOut)
def create_student(payload: StudentCreate, db: Session = Depends(database.get_db)):
    return service.create(db, payload)

@router.get("", response_model=List[StudentOut])
def list_students(db: Session = Depends(database.get_db)):
    return service.list(db)




@router.get("/me/enrolled-courses")
def get_enrolled_courses(
    student_id: int,
    organization_id: int,
    session_id: str,
    semester_id: str,
    db: Session = Depends(database.get_db)
):
    courses = service.get_enrolled_courses(
        db, student_id, organization_id, session_id, semester_id
    )

    if not courses:
        raise HTTPException(status_code=404, detail="No enrolled courses found")

    return {
        "success": True,
        "message": "Enrolled courses fetched successfully",
        "count": len(courses),
        "data": courses
    }