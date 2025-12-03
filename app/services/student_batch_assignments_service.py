from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from app.helper.dependencies import check_permission, get_current_user
from app.models.student_batch_assignments import StudentBatchAssignment
from app.models.student_batches import StudentBatch
from app.models.student import Student


def assign_students_to_batch_service(db: Session, batch_id: int, student_ids: List[int]):
    # Check batch exists
    batch = db.query(StudentBatch).filter(StudentBatch.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")

    # Check valid students
    students = db.query(Student).filter(Student.id.in_(student_ids)).all()
    if not students:
        raise HTTPException(status_code=404, detail="No valid students found")

    assigned_count = 0

    for student in students:
        exists = (
            db.query(StudentBatchAssignment)
            .filter(
                StudentBatchAssignment.student_id == student.id,
                StudentBatchAssignment.batch_id == batch_id,
            )
            .first()
        )
        if not exists:
            db.add(StudentBatchAssignment(student_id=student.id, batch_id=batch_id))
            assigned_count += 1

    db.commit()

    return {
        "success": True,
        "message": "Students assigned successfully",
        "batch_id": batch_id,
        "assigned_count": assigned_count,
    }


#Allows a student to enroll themselves into a batch.
def assign_student_self_enroll_service(db: Session, batch_id: int, student_id: int):


    batch = db.query(StudentBatch).filter(StudentBatch.id == batch_id).first()
    if not batch:
        return {"success": False, "message": "Batch not found"}

    existing = (
        db.query(StudentBatchAssignment)
        .filter(
            StudentBatchAssignment.batch_id == batch_id,
            StudentBatchAssignment.student_id == student_id,
        )
        .first()
    )
    if existing:
        return {"success": False, "message": "You are already enrolled in this batch"}

    new_assignment = StudentBatchAssignment(
        batch_id=batch_id,
        student_id=student_id,
    )
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)

    return {
        "success": True,
        "message": "Enrolled successfully",
        "batch_id": batch_id,
    }