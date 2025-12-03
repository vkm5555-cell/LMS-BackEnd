from sqlalchemy.orm import Session, aliased
from fastapi import APIRouter, Depends, UploadFile, File, Form
from app.models.course_chapter import CourseChapter
from app.models.chapter_content import ChapterContent
from app.models.student_course_progress import StudentCourseProgress
from app.schemas.course_chapter import CourseChaptersCreate
from datetime import datetime
from fastapi import UploadFile, HTTPException
import os
import uuid
from app.utils.pagination import paginate_query
from math import ceil
from app.utils.file_utils import save_uploaded_file

from sqlalchemy import text
BASE_URL: str = "http://localhost:8000/"



def create_multiple_chapters(db: Session, data: CourseChaptersCreate, user_id: int):
    new_chapters = []

    for ch in data.chapters:
        chapter = CourseChapter(
            course_id=data.course_id,
            user_id=user_id,
            chapter_name=ch.title,
            description=ch.description,
            order=ch.order,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        new_chapters.append(chapter)

    db.add_all(new_chapters)
    db.commit()

    return new_chapters


def get_chapters_by_course_id(
    db: Session,
    course_id: int,
    user_id: int,
    search: str = None,
    page: int = 1,
    limit: int = 10
    ):
    query = db.query(CourseChapter).filter(CourseChapter.course_id == course_id)

    if search:
        query = query.filter(CourseChapter.chapter_name.ilike(f"%{search}%"))

    if user_id :
        query = query.filter(CourseChapter.user_id == user_id)

    offset = (page - 1) * limit
    chapters = query.offset(offset).limit(limit).all()

    return chapters


def get_chapter_by_id(db: Session, chapter_id: int):
    return db.query(CourseChapter).filter(CourseChapter.id == chapter_id).first()


UPLOAD_DIR = "uploads/chapter_contents"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_file(file: UploadFile) -> str:
    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(await file.read())

    return filepath


async def create_chapter_content_service(
    db: Session,
    chapter_id: int,
    user_id: int,
    title: str,
    slug: str,
    description: str,
    content_type: str,
    content_url: str = None,
    content: str = None,
    content_file: UploadFile = File(None),
    video_duration: int = None,
    position: int = None,
    is_published: bool = False,
    is_free: bool = False,
    meta_data: str = None,
):

    content_path = None

    if content_file and content_file.filename:
        # file validation + save done inside utils
        content_path = await save_uploaded_file(content_file, directory="uploads/chapter_contents")

    final_content_url = content_path if content_path else content_url

    query = text("""
        INSERT INTO chapter_contents (
            chapter_id,
            user_id,
            title,
            slug,
            description,
            content_type,
            content_url,
            content,
            video_duration,
            position,
            is_published,
            is_free,
            meta_data,
            created_at,
            updated_at
        ) VALUES (
            :chapter_id,
            :user_id,
            :title,
            :slug,
            :description,
            :content_type,
            :content_url,
            :content,
            :video_duration,
            :position,
            :is_published,
            :is_free,
            :meta_data,
            NOW(),
            NOW()
        )
    """)

    result = db.execute(query, {
        "chapter_id": chapter_id,
        "user_id": user_id,
        "title": title,
        "slug": slug,
        "description": description,
        "content_type": content_type,
        "content_url": final_content_url,
        "content": content,
        "video_duration": video_duration,
        "position": position,
        "is_published": is_published,
        "is_free": is_free,
        "meta_data": meta_data,
    })

    db.commit()
    return result.lastrowid


# Get chapter content by the chapter id

def get_chapter_content_by_chapter_id(db: Session, chapter_id: int, user_id: int):

    query = text("""
        SELECT 
            cc.id,
            cc.chapter_id,
            cc.user_id,
            cc.title,
            cc.slug,
            cc.description,
            cc.content_type,
            cc.content_url,
            cc.content,
            cc.position,
            cc.is_published,
            cc.is_free,
            cc.meta_data,
            cc.video_duration,

            scp.complete_per,
            scp.is_completed,
            scp.student_id,
            scp.last_accessed

        FROM chapter_contents AS cc
        LEFT JOIN student_course_content_progress AS scp
            ON scp.content_id = cc.id AND scp.student_id = :student_id

        WHERE cc.chapter_id = :chapter_id
        ORDER BY cc.position ASC
    """)

    result = db.execute(
        query,
        {
            "chapter_id": chapter_id,
            "student_id": user_id
        }
    )

    contents = [dict(row._mapping) for row in result]

    if not contents:
        raise HTTPException(status_code=404, detail="No content found for this chapter")

    for item in contents:
        if item.get("content_url"):
            clean_path = item["content_url"].replace("\\", "/").lstrip("/")
            if item.get("content_type") == "file":
                item["content_url"] = f"{BASE_URL.rstrip('/')}/{clean_path}"
            else:
                item["content_url"] = clean_path

    return contents



# Update Chapter Content
async def update_chapter_content_service(
    db: Session,
    id: int,
    user_id: int,
    title: str,
    slug: str,
    description: str,
    content_type: str,
    content_url: str = None,
    content: str = None,
    content_file: UploadFile = File(None),
    video_duration: int = None,
    position: int = None,
    is_published: bool = False,
    is_free: bool = False,
    meta_data: str = None,
):
    # Handle file upload (optional)
    content_path = None
    if content_file and hasattr(content_file, "filename") and content_file.filename:
        content_path = await save_file(content_file)

    final_content_url = content_path if content_path else content_url

    query = text("""
        UPDATE chapter_contents
        SET
            user_id = :user_id,
            title = :title,
            slug = :slug,
            description = :description,
            content_type = :content_type,
            content_url = :content_url,
            content = :content,
            video_duration = :video_duration,
            position = :position,
            is_published = :is_published,
            is_free = :is_free,
            meta_data = :meta_data,
            updated_at = NOW()
        WHERE id = :id
    """)

    db.execute(query, {
        "id": id,
        "user_id": user_id,
        "title": title,
        "slug": slug,
        "description": description,
        "content_type": content_type,
        "content_url": final_content_url,
        "content": content,
        "video_duration": video_duration,
        "position": position,
        "is_published": is_published,
        "is_free": is_free,
        "meta_data": meta_data,
    })
    db.commit()

    return {"message": "Chapter content updated successfully"}


# Delete Chapter Content
async def delete_chapter_content_service(db: Session, content_id: int):
    query = db.execute(
        text("SELECT id FROM chapter_contents WHERE id = :id"),
        {"id": content_id}
    ).fetchone()

    if not query:
        return False

    db.execute(
        text("DELETE FROM chapter_contents WHERE id = :id"),
        {"id": content_id}
    )
    db.commit()
    return True

#Get Student course chapter
# def get_student_chapters_by_course_id(db: Session, course_id: int, student_id: int, search: str, page: int, limit: int):
#     query = db.query(CourseChapter).filter(CourseChapter.course_id == course_id)
#
#     if search:
#         query = query.filter(CourseChapter.chapter_name.ilike(f"%{search}%"))
#
#     # if user_id :
#     #     query = query.filter(CourseChapter.user_id == user_id)
#
#     return paginate_query(query, page, limit)
#################################################################################
def get_student_chapters_by_course_id(
    db: Session,
    course_id: int,
    student_id: int,
    search: str,
    page: int,
    limit: int
):
    # Query only CourseChapter table
    query = (
        db.query(CourseChapter)
        .filter(CourseChapter.course_id == course_id)
    )

    if search:
        query = query.filter(CourseChapter.chapter_name.ilike(f"%{search}%"))

    # Pagination
    offset = (page - 1) * limit
    results = query.offset(offset).limit(limit).all()
    total_items = query.count()
    total_pages = ceil(total_items / limit) if total_items else 1

    chapters = []

    for chapter in results:
        chapter_data = chapter.__dict__.copy()
        #chapter_data.pop("_sa_instance_state", None)

        # Fetch progress separately for each chapter
        progress = get_progress_by_content_id(db, chapter.id, student_id)

        chapter_data["progress"] = progress

        chapters.append(chapter_data)

    return {
        "total_pages": total_pages,
        "limit": limit,
        "total_items": len(chapters),
        "items": chapters
    }



def get_progress_by_content_id(db: Session, content_id: int, student_id: int):
    progress = (
        db.query(StudentCourseProgress)
        .filter(
            StudentCourseProgress.content_id == content_id,
            StudentCourseProgress.student_id == student_id
        )
        .first()
    )

    if not progress:
        return None

    data = progress.__dict__.copy()
    data.pop("_sa_instance_state", None)
    return data
####################################################################################
# def get_student_chapters_by_course_id(
#     db: Session,
#     course_id: int,
#     student_id: int,
#     search: str,
#     page: int,
#     limit: int
# ):
#     # 1️⃣ Get paginated chapters
#     query = db.query(CourseChapter).filter(CourseChapter.course_id == course_id)
#
#     if search:
#         query = query.filter(CourseChapter.chapter_name.ilike(f"%{search}%"))
#
#     total_items = query.count()
#     total_pages = ceil(total_items / limit) if total_items else 1
#     offset = (page - 1) * limit
#     chapters = query.offset(offset).limit(limit).all()
#
#     # 2️⃣ Get all content IDs for these chapters
#     chapter_ids = [c.id for c in chapters]
#     contents = (
#         db.query(ChapterContent.id, ChapterContent.chapter_id)
#         .filter(ChapterContent.chapter_id.in_(chapter_ids))
#         .all()
#     )
#
#     content_id_to_chapter = {c.id: c.chapter_id for c in contents}
#
#     # 3️⃣ Get student progress records for these contents
#     progress_records = (
#         db.query(
#             StudentCourseProgress.content_id,
#             StudentCourseProgress.complete_per,
#             StudentCourseProgress.is_completed,
#             StudentCourseProgress.last_accessed,
#         )
#         .filter(StudentCourseProgress.student_id == student_id)
#         .filter(StudentCourseProgress.content_id.in_([c.id for c in contents]))
#         .all()
#     )
#
#     # 4️⃣ Map progress by chapter_id
#     chapter_progress_map = {}
#     for record in progress_records:
#         chapter_id = content_id_to_chapter.get(record.content_id)
#         if not chapter_id:
#             continue
#
#         if chapter_id not in chapter_progress_map:
#             chapter_progress_map[chapter_id] = []
#
#         chapter_progress_map[chapter_id].append({
#             "content_id": record.content_id,
#             "complete_per": record.complete_per,
#             "is_completed": record.is_completed,
#             "last_accessed": record.last_accessed,
#         })
#
#     # 5️⃣ Combine chapter info + mapped progress
#     data = []
#     for ch in chapters:
#         data.append({
#             "chapter_id": ch.id,
#             "chapter_name": ch.chapter_name,
#             "description": ch.description,
#             "order": ch.order,
#             "progress": chapter_progress_map.get(ch.id, []),
#         })
#
#     return {
#         "page": page,
#         "limit": limit,
#         "total_pages": total_pages,
#         "total_items": total_items,
#         "items": data,
#     }

#Update course chapter by the id
def update_chapter_service(db: Session, chapter_id: int, chapter_name: str, description: str, user_id: int):
    from app.models.course_chapter import CourseChapter

    chapter = db.query(CourseChapter).filter(CourseChapter.id == chapter_id).first()

    if not chapter:
        return None

    # Optional: Only the creator can update
    if chapter.user_id != user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to update this chapter")

    chapter.chapter_name = chapter_name
    chapter.description = description
    db.commit()
    db.refresh(chapter)

    return chapter

##Get Student course chapter and completed course chapter
def get_course_content_completed_percentage_service(db: Session, course_id: int, student_id: int):

    # 1. Get all chapter IDs in the course
    chapter_ids = (
        db.query(CourseChapter.id)
        .filter(CourseChapter.course_id == course_id)
        .all()
    )
    chapter_ids = [c.id for c in chapter_ids]

    if not chapter_ids:
        return {
            "total_contents": 0,
            "completed_contents": 0,
            "completion_percentage": 0.0
        }

    # 2. Count total contents in these chapters
    total_contents = (
        db.query(ChapterContent)
        .filter(ChapterContent.chapter_id.in_(chapter_ids))
        .count()
    )

    # 3. Count completed contents from progress table
    completed_contents = (
        db.query(StudentCourseProgress)
        .filter(
    StudentCourseProgress.student_id == student_id,
            StudentCourseProgress.is_completed == True,
            StudentCourseProgress.course_id == course_id
        )
        .count()
    )

    # 4. Calculate percentage
    percentage = 0.0
    if total_contents > 0:
        percentage = round((completed_contents / total_contents) * 100, 2)

    return {
        "total_contents": total_contents,
        "completed_contents": completed_contents,
        "completion_percentage": percentage
    }


#Update course chapter by the id
def update_chapter_service(db: Session, chapter_id: int, chapter_name: str, description: str, user_id: int):
    from app.models.course_chapter import CourseChapter

    chapter = db.query(CourseChapter).filter(CourseChapter.id == chapter_id).first()

    if not chapter:
        return None

    # Optional: Only the creator can update
    if chapter.user_id != user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to update this chapter")

    chapter.chapter_name = chapter_name
    chapter.description = description
    db.commit()
    db.refresh(chapter)

    return chapter

# Get Student course chapter and completed course chapter by student id
# It is created for the student dasahboard
def get_student_course_content_completed_percentage_service(db: Session, student_id: int):

    # 1. Get all chapter IDs in the course
    chapter_ids = (
        db.query(CourseChapter.id)
       .all()
    )
    chapter_ids = [c.id for c in chapter_ids]

    if not chapter_ids:
        return {
            "total_contents": 0,
            "completed_contents": 0,
            "completion_percentage": 0.0
        }

    # 2. Count total contents in these chapters
    total_contents = (
        db.query(ChapterContent)
        .filter(ChapterContent.chapter_id.in_(chapter_ids))
        .count()
    )

    # 3. Count completed contents from progress table
    completed_contents = (
        db.query(StudentCourseProgress)
        .filter(
    StudentCourseProgress.student_id == student_id,
            StudentCourseProgress.is_completed == True,

        )
        .count()
    )

    # 4. Calculate percentage
    percentage = 0.0
    if total_contents > 0:
        percentage = round((completed_contents / total_contents) * 100, 2)

    return {
        "total_contents": total_contents,
        "completed_contents": completed_contents,
        "completion_percentage": percentage
    }

#Get chapter content detail by the chapter id
def get_chapter_content_by_id(db: Session, content_id: int):
    return db.query(ChapterContent).filter(ChapterContent.id == content_id).first()
