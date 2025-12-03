from sqlalchemy.orm import Session, joinedload
from app.models.student_batches import StudentBatch
from app.models.course import Course
from app.models.organization import Organization
from app.schemas.student_batches import StudentBatchCreate
from app.models.models import User
from app.models.student_batch_assignments import StudentBatchAssignment


def create_student_batch(db: Session, batch_data: StudentBatchCreate):

    existing_batch = db.query(StudentBatch).filter(
        StudentBatch.organization_id == batch_data.organization_id,
        StudentBatch.session_id == batch_data.session_id,
        StudentBatch.semester_id == batch_data.semester_id,
        StudentBatch.course_id == batch_data.course_id,
        StudentBatch.name == batch_data.name
    ).first()

    if existing_batch:
        return {"exists": True, "batch": existing_batch}

    new_batch = StudentBatch(**batch_data.dict())
    db.add(new_batch)
    db.commit()
    db.refresh(new_batch)
    return {"exists": False, "batch": new_batch}


def get_all_student_batches(db: Session, user_id: int):
    # Build custom SQLAlchemy query with LEFT JOINs
    query = (
        db.query(
            StudentBatch.id,
            StudentBatch.name,
            StudentBatch.description,
            StudentBatch.organization_id,
            Organization.org_name.label("organization_name"),
            StudentBatch.session_id,
            StudentBatch.semester_id,
            StudentBatch.course_id,
            Course.title.label("course_title"),
            StudentBatch.start_date,
            StudentBatch.end_date,
            StudentBatch.status,
            StudentBatch.created_at,
            StudentBatch.updated_at,
        )
        .outerjoin(Course, StudentBatch.course_id == Course.id)
        .outerjoin(Organization, StudentBatch.organization_id == Organization.id)
        .filter(StudentBatch.user_id == user_id)
        .order_by(StudentBatch.created_at.desc())
    )

    results = query.all()

    data = [
        {
            "id": row.id,
            "name": row.name,
            "description": row.description,
            "organization_id": row.organization_id,
            "organization_name": row.organization_name,
            "session_id": row.session_id,
            "semester_id": row.semester_id,
            "course_id": row.course_id,
            "course_title": row.course_title,
            "start_date": row.start_date,
            "end_date": row.end_date,
            "status": row.status,
            "created_at": row.created_at,
            "updated_at": row.updated_at,
        }
        for row in results
    ]

    return {
        "success": True,
        "message": "Student batches fetched successfully",
        "data": data,
    }

# Get batch detail by the batch id

def get_student_batch_by_id(db: Session, batch_id: int, user_id: int):
    return (
        db.query(StudentBatch)
        .filter(StudentBatch.id == batch_id, StudentBatch.user_id == user_id)
        .first()
    )

# Update batch

def update_student_batch(db: Session, batch_id: int, batch_data, user_id: int):
    from app.models.student_batches import StudentBatch  # adjust import if needed

    batch = (
        db.query(StudentBatch)
        .filter(StudentBatch.id == batch_id, StudentBatch.user_id == user_id)
        .first()
    )

    if not batch:
        return None

    # Update only provided fields
    batch.name = batch_data.name
    batch.description = batch_data.description
    batch.organization_id = batch_data.organization_id
    batch.session_id = batch_data.session_id
    batch.semester_id = batch_data.semester_id
    batch.course_id = batch_data.course_id
    batch.start_date = batch_data.start_date
    batch.end_date = batch_data.end_date
    batch.status = batch_data.status

    db.commit()
    db.refresh(batch)
    return batch


# Delete Batch
def delete_student_batch(db: Session, batch_id: int, user_id: int):
    from app.models.student_batches import StudentBatch  # adjust import path as needed

    batch = (
        db.query(StudentBatch)
        .filter(StudentBatch.id == batch_id, StudentBatch.user_id == user_id)
        .first()
    )

    if not batch:
        return None

    db.delete(batch)
    db.commit()
    return True

# Get batch enrolled student list
def get_students_by_batch_id(db: Session, batch_id: int, user_id: int):
    # Verify batch belongs to the current user's organization
    batch = db.query(StudentBatch).filter(StudentBatch.id == batch_id).first()
    if not batch:
        return None

    # Assuming there's a mapping table between batches and students, like `student_batch_students`
    students = (
        db.query(User)
        .join(StudentBatchAssignment, StudentBatchAssignment.student_id == User.id)
        .filter(StudentBatchAssignment.batch_id == batch_id)
        .all()
    )

    return students


# Get course batch by the course id
def get_batches_by_course_id_with_user(db, course_id: int, user_id: int):

    query = (
        db.query(StudentBatch)
        .options(joinedload(StudentBatch.user))  # eager load user relationship
        .filter(StudentBatch.course_id == course_id)
       # .filter(StudentBatch.user_id == user_id)  # restrict to current user's organization
        .all()
    )

    return query