from datetime import datetime
from sqlalchemy.orm import Session
from app.models.student_course_progress import StudentCourseProgress

def mark_content_read(
    db: Session,
    student_id: int,
    course_id: int,
    chapter_id: int,
    content_id: int,
    complete_per: str
):
    # Check if already exists
    existing = (
        db.query(StudentCourseProgress)
        .filter(
            StudentCourseProgress.student_id == student_id,
            StudentCourseProgress.course_id == course_id,
            StudentCourseProgress.chapter_id == chapter_id,
            StudentCourseProgress.content_id == content_id,
        )
        .first()
    )

    if existing:
        existing.complete_per = complete_per
        existing.is_completed = 1 if float(complete_per) >= 90 else 0
        existing.last_accessed = datetime.utcnow()
    else:
        new_entry = StudentCourseProgress(
            student_id=student_id,
            course_id=course_id,
            chapter_id=chapter_id,
            content_id=content_id,
            complete_per=complete_per,
            is_completed=1,
            last_accessed=datetime.utcnow(),
        )
        db.add(new_entry)

    db.commit()
    db.flush()
    return {"status": True, "message": "Progress saved successfully"}
