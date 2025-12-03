from sqlalchemy.orm import Session
from app.models.course_type import CourseType
from app.schemas.course_type import CourseTypeCreate

class CourseTypeService:
    def create(self, db: Session, course_type: CourseTypeCreate):
        db_course_type = CourseType(
            name=course_type.name,
            description=course_type.description,
            status=course_type.status,
        )
        db.add(db_course_type)
        db.commit()
        db.refresh(db_course_type)
        return db_course_type

    def list(self, db: Session):
        return db.query(CourseType).all()
