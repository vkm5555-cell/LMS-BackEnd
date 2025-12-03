from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.services.course_service import CourseService
from app.schemas.course import CourseCreate
from app.models.course import Course

class CourseController:

    @staticmethod
    def create(payload: CourseCreate, user_id: int, db: Session):
        try:
            course = CourseService.create_course(db, payload, user_id)
            return JSONResponse(
                content={
                    "success": True,
                    "course": {
                        "id": course.id,
                        "title": course.title,
                        "cafeteria": course.cafeteria,
                        "nsqf_level": course.nsqf_level,
                        "credit": course.credit,
                        "course_time": course.course_time,
                        "description": course.description,
                        "subtitle": course.subtitle,
                        "learning_objectives": course.learning_objectives,
                        "requirements": course.requirements,
                        "language": course.language,
                        "level": course.level,
                        "topic_tags": course.topic_tags,
                        "course_thumb": course.course_thumb,
                        "promo_video_url": course.promo_video_url,
                        "user_id": course.user_id,
                        "created_at": str(course.created_at),
                        "updated_at": str(course.updated_at),
                    },
                },
                status_code=201
            )
        except Exception as e:
            return JSONResponse(
                content={"success": False, "message": str(e)},
                status_code=500
            )

    @staticmethod
    def list(db, user_id: int, title=None, course_type=None, course_mode=None, category_id=None, skip=0, limit=10):
        return CourseService.list_courses(
            db=db,
            user_id=user_id,
            title=title,
            course_type=course_type,
            course_mode=course_mode,
            category_id=category_id,
            skip=skip,
            limit=limit
        )

    @staticmethod
    def adminCourseList(db, user_id: int, title=None, course_type=None, course_mode=None, category_id=None, skip=0, limit=10):
        return CourseService.adminCourseList(
            db=db,
            user_id=user_id,
            title=title,
            course_type=course_type,
            course_mode=course_mode,
            category_id=category_id,
            skip=skip,
            limit=limit
        )

    @staticmethod
    def get(course_id: int, user_id: int, db):
        return CourseService.get_course(db, course_id, user_id)

    @staticmethod
    def update(course_id: int, payload: dict, user_id: int, db):
        return CourseService.update_course(db, course_id, user_id, payload)

    @staticmethod
    def delete(course_id: int, user_id: int, db: Session):
        course = CourseService.delete_course(db, course_id, user_id)
        return course

    @staticmethod
    def get_latest_by_category(category_id: int, db: Session, limit: int = 3):
        return CourseService.get_latest_courses_by_category(db, category_id, limit)

    # Get singal course detail on the frontend
    @staticmethod
    def ViewCourse(id: int, db: Session):
        return CourseService.get_singal_course(db, id)

    @staticmethod
    def get_all(db: Session):
        return db.query(Course).order_by(Course.title.asc()).all()






