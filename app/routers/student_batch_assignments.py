from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.helper.dependencies import check_permission, get_current_user
from app.db.session import db as database
from app.services.student_batch_assignments_service import assign_students_to_batch_service, assign_student_self_enroll_service

router = APIRouter(prefix="/student-batches-assignments", tags=["Student Batch Assignments"])


class StudentBatchAssignmentCreate(BaseModel):
    student_ids: List[int]


class StudentBatchAssignmentResponse(BaseModel):
    message: str
    batch_id: int
    assigned_count: int


@router.post(
    "/{batch_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=StudentBatchAssignmentResponse,
)
def assign_students_to_batch(
    batch_id: int,
    body: StudentBatchAssignmentCreate,
    db: Session = Depends(database.get_db),
):
    result = assign_students_to_batch_service(db, batch_id, body.student_ids)
    return result

"""
    Allows a student to enroll themselves into a batch.
    Requires student authentication.
"""
@router.post(
    "/enroll/{batch_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Allow student to enroll themselves into a batch"
)
def student_self_enroll(
    batch_id: int,
    db: Session = Depends(database.get_db),
    authorization: str = Header(..., description="Bearer access token"),
):

    try:
        current_user = get_current_user(authorization, db)

        # Make sure current user is a student (optional role check)
        # if getattr(current_user, "role", None) not in ["student", "Student"]:
        #     raise HTTPException(status_code=403, detail="Only students can enroll themselves")

        result = assign_student_self_enroll_service(db, batch_id, current_user.id)

        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])

        return {
            "success": True,
            "message": "Student enrolled successfully",
            "data": {
                "batch_id": result["batch_id"],
                "student_id": current_user.id,
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))