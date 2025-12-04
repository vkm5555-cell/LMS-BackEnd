import os
import shutil
from fastapi import UploadFile, HTTPException, Request
from sqlalchemy.orm import Session, joinedload
from app.models.course import Course
import uuid
from app.schemas.course import CourseCreate
from app.core.config import settings


class CourseService:
    UPLOAD_DIR = "uploads/course_thumbs/"  # define your uploads folder

    @staticmethod
    def save_file(file: UploadFile) -> str:
        """
        Save uploaded image file to disk with a unique name and return its path.
        Only allows image files.
        """
        if not file:
            return None

        # Validate file type
        allowed_types = ["image/png", "image/jpeg", "image/jpg", "image/gif", "image/webp"]
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Only image files are allowed")

        # Ensure directory exists
        os.makedirs(CourseService.UPLOAD_DIR, exist_ok=True)

        # Generate unique filename (UUID + extension)
        _, ext = os.path.splitext(file.filename)
        unique_name = f"{uuid.uuid4().hex}{ext}"
        file_path = os.path.join(CourseService.UPLOAD_DIR, unique_name)

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return file_path

    @staticmethod
    def create_course(db: Session, course_data: CourseCreate, user_id: int, course_thumb: UploadFile = None):
        """
        Create a new course linked to the user.
        Optionally upload course_thumb image.
        """
        #return course_data.description

        # 🔹 Create course
        course = Course(
            course_type=course_data.course_type,
            category_id=course_data.category_id,
            course_price=course_data.course_price,
            course_mode=course_data.course_mode,
            title=course_data.title,
            cafeteria=course_data.cafeteria,
            nsqf_level=course_data.nsqf_level,
            credit=course_data.credit,
            course_time = course_data.course_time,
            description=course_data.description,
            subtitle=course_data.subtitle,
            learning_objectives=course_data.learning_objectives,
            requirements=course_data.requirements,
            language=course_data.language,
            level=course_data.level,
            topic_tags=course_data.topic_tags,
            course_thumb=course_data.course_thumb,  # saved uploaded file path
            promo_video_url=course_data.promo_video_url,
            user_id=user_id
        )

        db.add(course)
        db.commit()
        db.refresh(course)
        return course


    @staticmethod
    def list_courses(db: Session, user_id: int, title=None, course_type=None, course_mode=None, category_id=None,
                     skip=0, limit=10):
        query = db.query(Course).options(
            joinedload(Course.category),
            joinedload(Course.user)
        )
        query = query.filter(Course.user_id == user_id)

        if title:
            query = query.filter(Course.title.ilike(f"%{title}%"))
        if course_type:
            query = query.filter(Course.course_type == course_type)
        if course_mode:
            query = query.filter(Course.course_mode == course_mode)
        if category_id:
            query = query.filter(Course.category_id == category_id)
        query = query.order_by(Course.created_at.desc())
        total = query.count()
        courses = query.offset(skip).limit(limit).all()

        items = []
        for c in courses:
            items.append({
                "id": c.id,
                "title": c.title,
                "description": c.description,
                "subtitle": c.subtitle,
                "language": c.language,
                "level": c.level,
                "course_type": c.course_type,
                "course_mode": c.course_mode,
                "course_price": str(c.course_price) if c.course_price else None,
                "category_id": c.category_id,
                "category_name": c.category.name if c.category else None,
                "user": {
                    "id": c.user.id,
                    "name": c.user.name,
                    "email": c.user.email,
                } if c.user else None,
                "created_at": c.created_at,
                "updated_at": c.updated_at
            })

        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "items": items
        }

    @staticmethod
    def adminCourseList(db: Session, user_id: int, title=None, course_type=None, course_mode=None, category_id=None,
                     skip=0, limit=10):
        query = db.query(Course).options(
            joinedload(Course.category),
            joinedload(Course.user)
        )
        #query = query.filter(Course.user_id == user_id)

        if title:
            query = query.filter(Course.title.ilike(f"%{title}%"))
        if course_type:
            query = query.filter(Course.course_type == course_type)
        if course_mode:
            query = query.filter(Course.course_mode == course_mode)
        if category_id:
            query = query.filter(Course.category_id == category_id)

        total = query.count()
        courses = query.offset(skip).limit(limit).all()

        items = []
        for c in courses:
            items.append({
                "id": c.id,
                "title": c.title,
                "description": c.description,
                "subtitle": c.subtitle,
                "language": c.language,
                "level": c.level,
                "course_type": c.course_type,
                "course_mode": c.course_mode,
                "course_price": str(c.course_price) if c.course_price else None,
                "category_id": c.category_id,
                "category_name": c.category.name if c.category else None,
                "user": {
                    "id": c.user.id,
                    "name": c.user.name,
                    "email": c.user.email,
                } if c.user else None,
                "created_at": c.created_at,
                "updated_at": c.updated_at
            })

        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "items": items
        }

    @staticmethod
    def get_course(db: Session, course_id: int, user_id: int):
        course = (
            db.query(Course)
            .options(joinedload(Course.category))  # eager load category
            .filter(Course.id == course_id, Course.user_id == user_id)
            .first()
        )
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        return course

    @staticmethod
    def update_course(db: Session, course_id: int, user_id: int, course_data: dict):
        course = db.query(Course).filter(Course.id == course_id, Course.user_id == user_id).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        for field, value in course_data.items():
            if value is not None:  # only update provided values
                setattr(course, field, value)

        db.commit()
        db.refresh(course)
        return course

    @staticmethod
    def delete_course(db: Session, course_id: int, user_id: int):
        course = db.query(Course).filter(Course.id == course_id, Course.user_id == user_id).first()
        if not course:
            return None  # not found or not owned by user

        db.delete(course)
        db.commit()
        return course


    @staticmethod
    def get_latest_courses_by_category(db: Session, category_id: int, limit: int = 3):
        query = (
            db.query(Course)
            .options(
                joinedload(Course.category),
                joinedload(Course.user)
            )
            .filter(Course.category_id == category_id)
            .order_by(Course.created_at.desc())
            .limit(limit)
        )

        courses = query.all()
        items = []
        for c in courses:
            items.append({
                "id": c.id,
                "title": c.title,
                "description": c.description,
                "subtitle": c.subtitle,
                "language": c.language,
                "level": c.level,
                "course_type": c.course_type,
                "course_mode": c.course_mode,
                "course_price": str(c.course_price) if c.course_price else None,
                "category_id": c.category_id,
                "category_name": c.category.name if c.category else None,
                "course_thumb": c.course_thumb,
                "promo_video_url": c.promo_video_url,
                "created_at": c.created_at,
                "updated_at": c.updated_at,
                "user": {
                    "id": c.user.id,
                    "name": c.user.name if hasattr(c.user, "name") else None,
                    "email": c.user.email if hasattr(c.user, "email") else None
                } if c.user else None
            })

        return items

    # Get Singal Course details on the frontend
    @staticmethod
    def get_singal_course(db: Session, id: int, request: Request = None):
        course = (
            db.query(Course)
            .options(
                joinedload(Course.category),
                joinedload(Course.user)
            )
            .filter(Course.id == id)
            .first()
        )

        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        BASE_URL = settings.BASE_URL.rstrip()
        if course.course_thumb:
            # Use dynamic base URL if request is available
            base_url = str(request.base_url).rstrip() if request else BASE_URL
            if not course.course_thumb.startswith("http"):
                course_thumb_url = f"{base_url}/{course.course_thumb.lstrip('/')}"
            else:
                course_thumb_url = course.course_thumb
        else:
            course_thumb_url = None

        return {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "learning_objectives": course.learning_objectives,
            "subtitle": course.subtitle,
            "language": course.language,
            "level": course.level,
            "course_type": course.course_type,
            "course_mode": course.course_mode,
            "course_price": str(course.course_price) if course.course_price else None,
            "category_id": course.category_id,
            "category_name": course.category.name if course.category else None,
            "course_thumb": course_thumb_url,
            "promo_video_url": course.promo_video_url,
            "created_at": course.created_at,
            "updated_at": course.updated_at,
            "user": {
                "id": course.user.id,
                "name": getattr(course.user, "name", None),
                "email": getattr(course.user, "email", None)
            } if course.user else None
        }