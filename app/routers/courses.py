from fastapi import APIRouter, Depends, Header, UploadFile, File, Form, Query, HTTPException
from sqlalchemy.orm import Session
from app.services.course_service import CourseService
from app.db.session import db as database
from app.schemas.course import CourseCreate, CourseOut
from app.helper.dependencies import check_permission, get_current_user
from app.controllers.course_controller import CourseController


router = APIRouter()
@router.post("/courses")
@router.post("/courses")
async def create_course(
    # Text fields
    course_type: str = Form(...),
    course_price: str = Form(...),
    course_mode: str = Form(...),
    title: str = Form(...),
    cafeteria: str = Form(...),
    nsqf_level: str = Form(...),
    credit: str = Form(...),
    course_time: str = Form(...),
    slug: str = Form(...),
    subtitle: str = Form(...),
    description: str = Form(...),
    learning_objectives: str = Form(...),
    requirements: str = Form(...),
    category_id: int = Form(...),
    level: str = Form(...),
    language: str = Form(...),
    subtitle_languages: str = Form(...),
    topic_tags: str = Form(...),
    # File field
    course_thumb: UploadFile = File(...),
    # Auth + DB
    authorization: str = Header(...),
    db: Session = Depends(database.get_db)
):

    course_thumb_path = CourseService.save_file(course_thumb)

    # Build payload for DB (don’t pass UploadFile directly)
    payload = CourseCreate(
        course_type = course_type,
        category_id = category_id,
        course_price = course_price,
        course_mode = course_mode,
        title=title,
        cafeteria=cafeteria,
        nsqf_level=nsqf_level,
        credit=credit,
        course_time=course_time,
        slug=slug,
        subtitle = subtitle,
        description=description,
        learning_objectives=learning_objectives,
        requirements = requirements,
        level=level,
        language=language,
        subtitle_languages=subtitle_languages,
        topic_tags=topic_tags,
        course_thumb=course_thumb_path,  # store path or URL
    )

    # Save course (example: controller/service)
    current_user = get_current_user(authorization, db)
    new_course = CourseController.create(payload, current_user.id, db)

    return {
        "success": True,
        "message": "Course created successfully",
        "data": new_course  # JSON safe
    }


@router.get("/courses")
async def list_courses(
    # Filters
    title: str | None = Query(None, description="Search by title"),
    course_type: str | None = Query(None, description="Filter by course type"),
    course_mode: str | None = Query(None, description="Filter by course mode"),
    category_id: int | None = Query(None, description="Filter by category id"),
    # Pagination
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    # Auth + DB
    authorization: str = Header(...),
    db: Session = Depends(database.get_db)
):
    current_user = get_current_user(authorization, db)
    result = CourseController.list(
        db=db,
        user_id=current_user.id,
        title=title,
        course_type=course_type,
        course_mode=course_mode,
        category_id=category_id,
        skip=skip,
        limit=limit
    )
    return result
    return {
        "success": True,
        "message": "Courses fetched successfully",
        "data": result
    }


@router.get("/courses/adminCourseList")
async def list_courses(
    # Filters
    title: str | None = Query(None, description="Search by title"),
    course_type: str | None = Query(None, description="Filter by course type"),
    course_mode: str | None = Query(None, description="Filter by course mode"),
    category_id: int | None = Query(None, description="Filter by category id"),
    # Pagination
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    # Auth + DB
    authorization: str = Header(...),
    db: Session = Depends(database.get_db)
):
    current_user = get_current_user(authorization, db)
    result = CourseController.adminCourseList(
        db=db,
        user_id=current_user.id,
        title=title,
        course_type=course_type,
        course_mode=course_mode,
        category_id=category_id,
        skip=skip,
        limit=limit
    )
    return result
    return {
        "success": True,
        "message": "Courses fetched successfully",
        "data": result
    }





@router.get("/courses/{id}")
async def get_course_detail(
    id: int,
    authorization: str = Header(...),
    db: Session = Depends(database.get_db)
):
    current_user = get_current_user(authorization, db)
    course = CourseController.get(id, current_user.id, db)



    return {
        "success": True,
        "message": "Course fetched successfully",
        "data": {
            "id": course.id,
            "title": course.title,
            "slug": course.slug,
            "subtitle": course.subtitle,
            "description": course.description,
            "learning_objectives": course.learning_objectives,
            "requirements": course.requirements,
            "language": course.language,
            "level": course.level,
            "course_type": course.course_type,
            "course_mode": course.course_mode,
            "cafeteria": course.cafeteria,
            "nsqf_level": course.nsqf_level,
            "credit": course.credit,
            "course_time": course.course_time,
            "course_price": str(course.course_price) if course.course_price else None,
            "topic_tags": course.topic_tags,
            "course_thumb": course.course_thumb,
            "promo_video_url": course.promo_video_url,
            "category_id": course.category_id,
            "category_name": course.category.name if course.category else None,
            "created_at": course.created_at,
            "updated_at": course.updated_at,
        }
    }


@router.put("/courses/{course_id}")
async def update_course(
    course_id: int,
    course_type: str | None = Form(None),
    course_price: str | None = Form(None),
    course_mode: str | None = Form(None),
    title: str | None = Form(None),
    subtitle: str | None = Form(None),
    description: str | None = Form(None),
    learning_objectives: str | None = Form(None),
    requirements: str | None = Form(None),
    category_id: int | None = Form(None),
    level: str | None = Form(None),
    language: str | None = Form(None),
    subtitle_languages: str | None = Form(None),
    topic_tags: str | None = Form(None),
    course_thumb: UploadFile | None = File(None),  # optional
    authorization: str = Header(...),
    db: Session = Depends(database.get_db)
):
    current_user = get_current_user(authorization, db)

    # Handle image upload
    course_thumb_path = None
    if course_thumb:  # only save if a new file is uploaded
        course_thumb_path = CourseService.save_file(course_thumb)

    payload = {
        "course_type": course_type,
        "course_price": course_price,
        "course_mode": course_mode,
        "title": title,
        "subtitle": subtitle,
        "description": description,
        "learning_objectives": learning_objectives,
        "requirements": requirements,
        "category_id": category_id,
        "level": level,
        "language": language,
        "subtitle_languages": subtitle_languages,
        "topic_tags": topic_tags,
        "course_thumb": course_thumb_path if course_thumb_path else None,
    }

    updated_course = CourseController.update(course_id, payload, current_user.id, db)

    return {
        "success": True,
        "message": "Course updated successfully",
        "data": updated_course
    }


@router.delete("/courses/{id}")
async def delete_course(
    id: int,
    authorization: str = Header(...),
    db: Session = Depends(database.get_db)
):
    current_user = get_current_user(authorization, db)

    course = CourseController.delete(id, current_user.id, db)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found or not owned by you")

    return {
        "success": True,
        "message": "Course deleted successfully",
        "data": {"id": id, "title": course.title}
    }



@router.get("/courses/by-category/{category_id}/latest")
async def get_latest_courses_by_category(
    category_id: int,
    limit: int = Query(3, ge=1, le=20, description="Number of latest courses to fetch"),
    db: Session = Depends(database.get_db)
):
    result = CourseController.get_latest_by_category(category_id, db, limit)
    return {
        "success": True,
        "message": f"Latest {limit} courses fetched successfully",
        "data": result
    }

# Get course details on the frontend
@router.get("/courses/view/{id}")
async def get_course_detail(
    id: int,
    db: Session = Depends(database.get_db)
):
    course = CourseController.ViewCourse(id, db)
    return course


@router.get("/courses/list/all", summary="Get all courses for dropdown")
async def get_all_courses_for_dropdown(
    db: Session = Depends(database.get_db)
):
    courses = CourseController.get_all(db)
    return {
        "success": True,
        "message": "All courses fetched successfully",
        "data": [
            {"id": c.id, "title": c.title}
            for c in courses
        ]
    }




