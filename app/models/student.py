# app/models/student.py
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.student_batch_assignments import StudentBatchAssignment
# Many-to-many enrollments table
from .course import Course  # import Course only if needed

# enrollments = Table(
#     "enrollments", Base.metadata,
#     Column("student_id", Integer, ForeignKey("students.id", ondelete="CASCADE"), primary_key=True),
#     Column("course_id", Integer, ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True),
# )


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True)

    # courses = relationship(
    #     "Course",
    #     secondary=enrollments,
    #     back_populates="students"
    # )
    #batch_assignments = relationship("StudentBatchAssignment", back_populates="student", cascade="all, delete-orphan")