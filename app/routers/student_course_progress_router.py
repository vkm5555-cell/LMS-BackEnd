from fastapi import APIRouter, Depends, Header, Form, HTTPException
from sqlalchemy.orm import Session
from app.db.session import db as database
from app.services.student_course_progress_service import mark_content_read
from app.helper.dependencies import check_permission, get_current_user


router = APIRouter(prefix="/student-course-progress", tags=["Users"])


@router.post("/mark-read")
async def mark_course_content_read(
    course_id: int = Form(...),
    chapter_id: int = Form(...),
    content_id: int = Form(...),
    percentage: str = Form(...),
    db: Session = Depends(database.get_db),
    authorization: str = Header(...),
):
    current_user = get_current_user(authorization, db)

    try:
        result = mark_content_read(
            db=db,
            student_id=current_user.id,
            course_id=course_id,
            chapter_id=chapter_id,
            content_id=content_id,
            complete_per=percentage
        )
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))