from sqlalchemy import Column, Integer, String, Text, DateTime, func, Enum
from app.db.base_class import Base
import enum

# Define Python Enum for status
class AssignmentStatus(str, enum.Enum):
    Active = "Active"
    Inactive = "Inactive"
    Deleted = "Deleted"

class CourseAssignment(Base):
    __tablename__ = "course_assignments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    course_id = Column(Integer, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    file_path = Column(String(500), nullable=True)
    max_marks = Column(Integer, default=100)
    due_date = Column(DateTime, nullable=True)

    # Status column as ENUM
    status = Column(
        Enum(AssignmentStatus, name="assignment_status_enum"),
        default=AssignmentStatus.Active,
        nullable=False
    )

    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


