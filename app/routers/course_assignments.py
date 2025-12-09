from fastapi import APIRouter, Depends, Header, Form, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any

from app.db.session import db as database
from app.schemas.course_assignment import CourseAssignmentCreate, CourseAssignmentUpdate
from app.services.course_assignment import CourseAssignmentService
from app.helper.dependencies import get_current_user


router = APIRouter(prefix="/course-assignments", tags=["Course Assignments"])


# ------------------------- CREATE -------------------------
@router.post("/")
async def create_assignment(
    course_id: int = Form(...),
    title: str = Form(...),
    description: str = Form(""),
    due_date: str = Form(None),
    max_marks: int = Form(100),
    file_path: UploadFile = File(None),
    authorization: str = Header(...),
    db: Session = Depends(database.get_db)
):
    try:
        current_user = get_current_user(authorization, db)
        service = CourseAssignmentService(db)

        payload: Dict[str, Any] = {
            "user_id": current_user.id,
            "course_id": course_id,
            "title": title,
            "description": description,
            "due_date": due_date,
            "max_marks": max_marks,
        }

        created = await service.create_assignment(payload, file=file_path)
        return {"success": True, "message": "Assignment created successfully", "data": created}

    except Exception as e:
        return {"success": False, "message": str(e), "data": None}


# ------------------------- LIST WITH PAGINATION & SEARCH -------------------------
@router.get("/")
def list_assignments(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    course_id: Optional[int] = Query(None),
    db: Session = Depends(database.get_db)
):
    try:
        service = CourseAssignmentService(db)
        result = service.get_assignments(page, limit, search, course_id)

        return {
            "success": True,
            "message": "Assignments fetched successfully",
            "page": result["page"],
            "limit": result["limit"],
            "total": result["total"],
            "total_pages": result["total_pages"],
            "data": result["items"]
        }

    except Exception as e:
        return {"success": False, "message": str(e), "data": None}


# ------------------------- GET BY ID -------------------------
@router.get("/{assignment_id}")
def get_assignment(assignment_id: int, db: Session = Depends(database.get_db)):
    try:
        service = CourseAssignmentService(db)
        assignment = service.get_assignment(assignment_id)
        if not assignment:
            return {"success": False, "message": "Assignment not found", "data": None}

        return {"success": True, "message": "Assignment fetched", "data": assignment}

    except Exception as e:
        return {"success": False, "message": str(e), "data": None}


# ------------------------- UPDATE -------------------------
# ------------------------- UPDATE -------------------------
@router.put("/{assignment_id}")
async def update_assignment(
    assignment_id: int,
    course_id: Optional[int] = Form(None),
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    due_date: Optional[str] = Form(None),
    max_marks: Optional[int] = Form(None),
    file_path: Optional[UploadFile] = File(None),
    authorization: str = Header(...),
    db: Session = Depends(database.get_db)
):
    try:
        current_user = get_current_user(authorization, db)
        service = CourseAssignmentService(db)

        # Prepare payload only with provided values
        payload: Dict[str, Any] = {}
        if course_id is not None:
            payload["course_id"] = course_id
        if title is not None:
            payload["title"] = title
        if description is not None:
            payload["description"] = description
        if due_date is not None:
            payload["due_date"] = due_date
        if max_marks is not None:
            payload["max_marks"] = max_marks
        payload["user_id"] = current_user.id  # optional: track who updated

        updated = await service.update_assignment(assignment_id, payload, file=file_path)
        if not updated:
            return {"success": False, "message": "Assignment not found", "data": None}

        return {"success": True, "message": "Assignment updated successfully", "data": updated}

    except Exception as e:
        return {"success": False, "message": str(e), "data": None}



# ------------------------- DELETE -------------------------
@router.delete("/{assignment_id}")
def delete_assignment(assignment_id: int, db: Session = Depends(database.get_db)):
    try:
        service = CourseAssignmentService(db)
        deleted = service.delete_assignment(assignment_id)
        if not deleted:
            return {"success": False, "message": "Assignment not found", "data": None}

        return {"success": True, "message": "Assignment deleted", "data": None}

    except Exception as e:
        return {"success": False, "message": str(e), "data": None}
