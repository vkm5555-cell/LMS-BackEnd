from fastapi import APIRouter, Depends, Header, Query, Form, File, UploadFile, HTTPException, Body
from sqlalchemy.orm import Session
from app.db.session import db as database
from app.schemas.course_chapter import CourseChaptersCreate, CourseChapterResponse
from app.schemas.chapter_content import ChapterContentCreate
from app.services import course_chapter_service as service
from app.helper.dependencies import check_permission, get_current_user
from pydantic import BaseModel
from typing import List, Optional
import json

router = APIRouter(prefix="/chapters", tags=["Course Chapters"])


@router.post("/bulk", response_model=List[CourseChapterResponse])
def create_multiple_chapters(
    data: CourseChaptersCreate,
    db: Session = Depends(database.get_db),
    authorization: str = Header(...),
):
    current_user = get_current_user(authorization, db)

    chapters = service.create_multiple_chapters(db, data, current_user.id)

    return chapters


#update course chapter by the id
@router.put("/{chapter_id}/update")
def update_course_chapter(
    chapter_id: int,
    chapter_name: str = Form(...),
    description: str = Form(...),
    db: Session = Depends(database.get_db),
    authorization: str = Header(...),
):

    current_user = get_current_user(authorization, db)

    try:
        updated_chapter = service.update_chapter_service(
            db=db,
            chapter_id=chapter_id,
            chapter_name=chapter_name,
            description=description,
            user_id=current_user.id
        )

        if not updated_chapter:
            raise HTTPException(status_code=404, detail="Chapter not found")

        return {
            "status": True,
            "message": "Chapter updated successfully",
            "data": updated_chapter
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-course/{course_id}")
def get_chapters_by_course_id(
    course_id: int,
    db: Session = Depends(database.get_db),
    authorization: str = Header(...),
    search: Optional[str] = Query(None, description="Search by chapter title"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
):

    current_user = get_current_user(authorization, db)
    #return current_user

    chapters = service.get_chapters_by_course_id(db, course_id, current_user.id, search, page, limit)
    return chapters


@router.get("/chaptergetbyid/{chapter_id}", response_model=CourseChapterResponse)
def get_single_chapter(
    chapter_id: int,
    db: Session = Depends(database.get_db),
    authorization: str = Header(...),
):

    current_user = get_current_user(authorization, db)

    chapter = service.get_chapter_by_id(db, chapter_id)

    if not chapter:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Chapter not found")

    if chapter.user_id != current_user.id:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="You are not authorized to view this chapter")

    return chapter


## Add Chapter Content


@router.post("/{chapter_id}/contents")
async def create_chapter_content(
    chapter_id: int,
    title: str = Form(...),
    slug: str = Form(...),
    description: str = Form(...),
    content_type: str = Form(...),
    content_url: str = Form(None),
    content: str = Form(None),
    position: int = Form(...),
    is_published: bool = Form(...),
    is_free: bool = Form(...),
    user_id: int = Form(...),
    meta_data: str = Form(...),
    video_duration: Optional[int] = Form(...),
    db: Session = Depends(database.get_db),
    authorization: Optional[str] = Header(None),
    content_file: UploadFile = File(None)
):
    try:

        new_content = await service.create_chapter_content_service(
            db=db,
            chapter_id=chapter_id,
            user_id=user_id,
            title=title,
            slug=slug,
            description=description,
            content_type=content_type,
            content_url=content_url,
            content=content,
            video_duration=video_duration,
            position=position,
            is_published=is_published,
            is_free=is_free,
            meta_data=meta_data,
            content_file=content_file
        )

        return {
            "status": True,
            "message": "Chapter content created successfully",

        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get Chapter Content by the chapter Id
@router.get("/{chapter_id}/contents")
async def get_chapter_content(
        chapter_id: int,
        db: Session = Depends(database.get_db),
        authorization: Optional[str] = Header(None),
):
    current_user = get_current_user(authorization, db)

    contents = service.get_chapter_content_by_chapter_id(db, chapter_id, current_user.id)

    return {
        "status": True,
        "message": "Chapter contents fetched successfully",
        "data": contents
    }

# Update Chapter Content
@router.post("/chapter-contents/{id}")
async def update_chapter_content(
    id: int,
    title: str = Form(...),
    slug: str = Form(...),
    description: str = Form(...),
    content_type: str = Form(...),
    content_url: str = Form(None),
    content: str = Form(None),
    position: int = Form(...),
    is_published: bool = Form(...),
    is_free: bool = Form(...),
    user_id: int = Form(...),
    meta_data: str = Form(...),
    video_duration: Optional[int] = Form(...),
    db: Session = Depends(database.get_db),
    authorization: Optional[str] = Header(None),
    content_file: UploadFile = File(None)
):
    #return id
    try:

        new_content = await service.update_chapter_content_service(
            db=db,
            id=id,
            user_id=user_id,
            title=title,
            slug=slug,
            description=description,
            content_type=content_type,
            content_url=content_url,
            content=content,
            video_duration=video_duration,
            position=position,
            is_published=is_published,
            is_free=is_free,
            meta_data=meta_data,
            content_file=content_file
        )

        return {
            "status": True,
            "message": "Chapter content created successfully",

        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Delete Chapter Content

@router.delete("/chapter-delete-contents/{id}")
async def delete_chapter_content(
        id: int,
        db: Session = Depends(database.get_db),
        authorization: str | None = Header(None)
):

    try:
        success = await service.delete_chapter_content_service(db, id)
        if not success:
            raise HTTPException(status_code=404, detail="Chapter content not found")
        return {"status": True, "message": "Chapter content deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#Get Student course chapter

@router.get("/student-course/{course_id}")
def get_chapters_by_course_id(
    course_id: int,
    db: Session = Depends(database.get_db),
    authorization: str = Header(...),
    search: Optional[str] = Query(None, description="Search by chapter title"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
):

    current_user = get_current_user(authorization, db)
    #return current_user

    chapters = service.get_student_chapters_by_course_id(db, course_id, current_user.id, search, page, limit)
    return chapters


#Get Student course chapter and completed course chapter
@router.get("/content-totals/{course_id}")
def get_course_content_completed_percentage(
    course_id: int,
    studentId: int,
    db: Session = Depends(database.get_db)
):
    chapters = service.get_course_content_completed_percentage_service(db, course_id, studentId)
    return chapters


# Get Student course chapter and completed course chapter by student id
# It is created for the student dasahboard
@router.get("/content-student-totals")
def get_course_content_completed_percentage(
    authorization: str = Header(...),
    db: Session = Depends(database.get_db)
):
    current_user = get_current_user(authorization, db)
    chapters = service.get_student_course_content_completed_percentage_service(db,  current_user.id)
    return chapters

#Get chapter content detail by the chapter id
@router.get("/chapter-content/{content_id}")
async def get_chapter_content_detail(
    content_id: int,
    db: Session = Depends(database.get_db),
    authorization: str = Header(...),
):
    # Authenticate user
    current_user = get_current_user(authorization, db)

    # Fetch content from service
    content = service.get_chapter_content_by_id(db, content_id)

    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    # # Optional: check ownership
    # if content.user_id != current_user.id:
    #     raise HTTPException(status_code=403, detail="You are not authorized to view this content")

    return {
        "status": True,
        "message": "Chapter content details fetched successfully",
        "data": content
    }