from sqlalchemy.orm import Session
from .base import BaseRepository
from app.models.student import Student
from app.models.course import Course

class CourseRepository(BaseRepository[Course]):
    def __init__(self):
        super().__init__(Course)

    def enroll_student(self, db: Session, course_id: int, student_id: int) -> bool:
        course = db.query(Course).filter(Course.id == course_id).first()
        student = db.query(Student).filter(Student.id == student_id).first()
        if not course or not student:
            return False
        if student not in course.students:
            course.students.append(student)
            db.commit()
        return True
