from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, func
from app.models.course_assignment import CourseAssignment
from app.utils.file_utils import save_uploaded_file
from fastapi import UploadFile
from typing import Optional, Dict, Any
from app.services.course_service import CourseService


class CourseAssignmentService:
    def __init__(self, db: Session):
        self.db = db

    # CREATE
    async def create_assignment(
        self,
        payload: Dict[str, Any],
        file: Optional[UploadFile] = None
    ) -> CourseAssignment:
        if file and file.filename:
            file_path = await save_uploaded_file(file, directory="uploads/course_assignments/")
            payload["file_path"] = file_path

        assignment = CourseAssignment(**payload)
        self.db.add(assignment)
        self.db.commit()
        self.db.refresh(assignment)
        return assignment

    # GET ALL with pagination & search
    def get_assignments(
            self,
            page: int = 1,
            limit: int = 10,
            search: Optional[str] = None,
            course_id: Optional[int] = None
    ):

        query = self.db.query(CourseAssignment).filter(CourseAssignment.deleted_at.is_(None))
        if course_id:
            query = query.filter(CourseAssignment.course_id == course_id)

        if search:
            query = query.filter(
                or_(
                    CourseAssignment.title.ilike(f"%{search}%"),
                    CourseAssignment.description.ilike(f"%{search}%")
                )
            )

        total = query.count()

        items = (
            query.order_by(CourseAssignment.id.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        # Attach course details per assignment
        response_items = []
        for assignment in items:
            course_data = CourseService.get_singal_course(
                db=self.db,
                id=assignment.course_id,
                request=None
            )

            response_items.append({
                "id": assignment.id,
                "course_id": assignment.course_id,
                "title": assignment.title,
                "description": assignment.description,
                "max_marks": assignment.max_marks,
                "due_date": assignment.due_date,
                "file_path": assignment.file_path,
                "created_at": assignment.created_at,
                "updated_at": assignment.updated_at,
                "course": course_data
            })

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": (total + limit - 1) // limit,
            "items": response_items
        }

    # GET BY ID
    def get_assignment(self, assignment_id: int) -> Optional[CourseAssignment]:
        return self.db.query(CourseAssignment).filter(CourseAssignment.id == assignment_id).first()

    # UPDATE
    async def update_assignment(
            self,
            assignment_id: int,
            data: Dict[str, Any],
            file: Optional[UploadFile] = None
    ) -> Optional[CourseAssignment]:
        assignment = self.get_assignment(assignment_id)
        if not assignment:
            return None

        # Handle file upload if provided
        if file and file.filename:
            file_path = await save_uploaded_file(file, directory="uploads/course_assignments/")
            data["file_path"] = file_path

        # Update fields
        for field, value in data.items():
            setattr(assignment, field, value)

        self.db.commit()
        self.db.refresh(assignment)
        return assignment

    # DELETE
    # SOFT DELETE (sets deleted_at instead of deleting row)
    def delete_assignment(self, assignment_id: int) -> bool:
        assignment = self.get_assignment(assignment_id)
        if not assignment:
            return False
        assignment.status = 'Deleted'
        assignment.deleted_at = func.now()
        self.db.commit()
        return True
