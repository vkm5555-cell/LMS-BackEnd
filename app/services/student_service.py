from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.student import StudentCreate
from app.repositories.student_repo import StudentRepository
from app.core.config import settings   # <-- import BASE_URL

class StudentService:
    def __init__(self, repo: StudentRepository | None = None):
        self.repo = repo or StudentRepository()

    def create(self, db: Session, data: StudentCreate):
        return self.repo.create(db, name=data.name, email=data.email)

    def list(self, db: Session):
        return self.repo.list(db)

    def get_enrolled_courses(
        self, db: Session, student_id: int, organization_id: int, session_id: str, semester_id: str
    ):
        query = text("""
            SELECT 
                c.*,                             
                sb.id AS batch_id,
                sb.name AS batch_name,
                sb.description AS batch_description,
                sb.session_id,
                sb.semester_id,
                sb.organization_id,
                sb.start_date,
                sb.end_date,
                sb.status AS batch_status
            FROM student_batches sb
            INNER JOIN student_batch_assignments sba 
                ON sb.id = sba.batch_id
            INNER JOIN courses c 
                ON sb.course_id = c.id
            WHERE 
                sba.student_id = :student_id
                AND sb.organization_id = :organization_id
                AND sb.session_id = :session_id
                AND sb.semester_id = :semester_id
        """)

        result = db.execute(
            query,
            {
                "student_id": student_id,
                "organization_id": organization_id,
                "session_id": session_id,
                "semester_id": semester_id,
            },
        ).fetchall()

        records = [dict(row._mapping) for row in result]

        # Add full image URL
        BASE_URL = settings.BASE_URL.rstrip("/")

        for item in records:
            if item.get("course_thumb"):
                item["course_thumb"] = f"{BASE_URL}/{item['course_thumb']}"
            else:
                item["course_thumb"] = None

        return records
