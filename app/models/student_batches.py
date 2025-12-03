from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, ForeignKey, func
from app.models.base import Base
from sqlalchemy.orm import relationship


class StudentBatch(Base):
    __tablename__ = "student_batches"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    organization_id = Column(Integer, nullable=False)
    session_id = Column(String(50), nullable=False)
    semester_id = Column(String(50), nullable=False)
    course_id = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(Enum("active", "inactive", name="batch_status"), default="active")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    student_assignments = relationship("StudentBatchAssignment", back_populates="batch", cascade="all, delete-orphan")
    user = relationship("User", back_populates="batches")