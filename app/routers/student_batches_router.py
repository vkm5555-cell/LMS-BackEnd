from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session
from app.db.session import db as database
from app.schemas.student_batches import StudentBatchCreate
from app.services.student_batches_service import create_student_batch, get_all_student_batches, get_student_batch_by_id, update_student_batch, delete_student_batch, get_students_by_batch_id, get_batches_by_course_id_with_user
from app.helper.dependencies import get_current_user

router = APIRouter(prefix="/student-batches", tags=["Student Batches"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_student_batch(
    batch: StudentBatchCreate,
    db: Session = Depends(database.get_db),
    authorization: str = Header(..., description="Bearer access token")
):
    try:
        current_user = get_current_user(authorization, db)
        batch.user_id = current_user.id

        result = create_student_batch(db, batch)

        if result["exists"]:
            existing = result["batch"]
            return {
                "success": False,
                "message": "Batch already exists for this course, session, semester, and organization.",
                "data": {
                    "id": existing.id,
                    "name": existing.name,
                    "organization_id": existing.organization_id,
                    "session_id": existing.session_id,
                    "semester_id": existing.semester_id,
                    "course_id": existing.course_id,
                    "status": existing.status,
                    "created_at": str(existing.created_at),
                    "updated_at": str(existing.updated_at)
                }
            }

        new_batch = result["batch"]
        return {
            "success": True,
            "message": "Student batch created successfully",
            "data": {
                "id": new_batch.id,
                "name": new_batch.name,
                "description": new_batch.description,
                "organization_id": new_batch.organization_id,
                "session_id": new_batch.session_id,
                "semester_id": new_batch.semester_id,
                "course_id": new_batch.course_id,
                "start_date": str(new_batch.start_date),
                "end_date": str(new_batch.end_date),
                "status": new_batch.status,
                "created_at": str(new_batch.created_at),
                "updated_at": str(new_batch.updated_at)
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/list/all", summary="Get all student batches")
def list_student_batches(
        db: Session = Depends(database.get_db),
        authorization: str = Header(..., description="Bearer access token")
):
    try:
        current_user = get_current_user(authorization, db)
        return get_all_student_batches(db, user_id=current_user.id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{batch_id}", summary="Get single student batch by ID")
def get_single_student_batch(
        batch_id: int,
        db: Session = Depends(database.get_db),
        authorization: str = Header(..., description="Bearer access token")
):
    try:
        current_user = get_current_user(authorization, db)
        batch = get_student_batch_by_id(db, batch_id=batch_id, user_id=current_user.id)

        if not batch:
            raise HTTPException(status_code=404, detail="Student batch not found")

        return {
            "success": True,
            "message": "Student batch retrieved successfully",
            "data": {
                "id": batch.id,
                "name": batch.name,
                "description": batch.description,
                "organization_id": batch.organization_id,
                "session_id": batch.session_id,
                "semester_id": batch.semester_id,
                "course_id": batch.course_id,
                "start_date": str(batch.start_date),
                "end_date": str(batch.end_date),
                "status": batch.status,
                "created_at": str(batch.created_at),
                "updated_at": str(batch.updated_at)
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{batch_id}", summary="Update an existing student batch")
def update_student_batch_api(
        batch_id: int,
        batch_data: StudentBatchCreate,  # reuse your create schema for updates
        db: Session = Depends(database.get_db),
        authorization: str = Header(..., description="Bearer access token")
):
    try:
        current_user = get_current_user(authorization, db)
        existing_batch = get_student_batch_by_id(db, batch_id=batch_id, user_id=current_user.id)

        if not existing_batch:
            raise HTTPException(status_code=404, detail="Student batch not found")

        updated_batch = update_student_batch(db, batch_id, batch_data, user_id=current_user.id)

        return {
            "success": True,
            "message": "Student batch updated successfully",
            "data": {
                "id": updated_batch.id,
                "name": updated_batch.name,
                "description": updated_batch.description,
                "organization_id": updated_batch.organization_id,
                "session_id": updated_batch.session_id,
                "semester_id": updated_batch.semester_id,
                "course_id": updated_batch.course_id,
                "start_date": str(updated_batch.start_date),
                "end_date": str(updated_batch.end_date),
                "status": updated_batch.status,
                "created_at": str(updated_batch.created_at),
                "updated_at": str(updated_batch.updated_at)
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{batch_id}", summary="Delete a student batch by ID")
def delete_student_batch_api(
        batch_id: int,
        db: Session = Depends(database.get_db),
        authorization: str = Header(..., description="Bearer access token")
):
    try:
        current_user = get_current_user(authorization, db)
        batch = get_student_batch_by_id(db, batch_id=batch_id, user_id=current_user.id)

        if not batch:
            raise HTTPException(status_code=404, detail="Student batch not found")

        # Delete the batch using service layer
        delete_student_batch(db, batch_id, user_id=current_user.id)

        return {
            "success": True,
            "message": "Student batch deleted successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Get batch enrolled student list
@router.get("/{batch_id}/students", summary="Get all students enrolled in a batch")
def get_students_in_batch(
        batch_id: int,
        db: Session = Depends(database.get_db),
        authorization: str = Header(..., description="Bearer access token")
):

    try:
        current_user = get_current_user(authorization, db)

        students = get_students_by_batch_id(db, batch_id=batch_id, user_id=current_user.id)

        if students is None:
            raise HTTPException(status_code=404, detail="Batch not found or you don't have access")

        return {
            "success": True,
            "message": "Students retrieved successfully",
            "data": [
                {
                    "id": s.id,
                    "name": s.name,
                    "email": s.email,
                    "roll_number": s.roll_number if hasattr(s, 'roll_number') else None,
                    "status": s.status if hasattr(s, 'status') else None,
                } for s in students
            ]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



# Get course batch by the course id
@router.get("/course/{course_id}", summary="Get all batches by course ID with user details")
def get_batches_by_course_id_api(
        course_id: int,
        db: Session = Depends(database.get_db),
        authorization: str = Header(..., description="Bearer access token")
):

    try:
        current_user = get_current_user(authorization, db)

        batches = get_batches_by_course_id_with_user(db, course_id=course_id, user_id=current_user.id)

        if not batches:
            raise HTTPException(status_code=404, detail="No batches found for this course")

        return {
            "success": True,
            "message": "Batches retrieved successfully",
            "data": [
                {
                    "id": b.id,
                    "name": b.name,
                    "description": b.description,
                    "organization_id": b.organization_id,
                    "session_id": b.session_id,
                    "semester_id": b.semester_id,
                    "course_id": b.course_id,
                    "start_date": str(b.start_date) if b.start_date else None,
                    "end_date": str(b.end_date) if b.end_date else None,
                    "status": b.status,
                    "created_at": str(b.created_at),
                    "updated_at": str(b.updated_at),
                    "user": {
                        "id": b.user.id if hasattr(b, "user") else None,
                        "name": b.user.name if hasattr(b, "user") else None,
                        "email": b.user.email if hasattr(b, "user") else None,
                    } if hasattr(b, "user") else None
                }
                for b in batches
            ]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))