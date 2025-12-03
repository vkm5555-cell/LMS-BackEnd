from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base import Base

class StudentBatchAssignment(Base):
    __tablename__ = "student_batch_assignments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    batch_id = Column(Integer, ForeignKey("student_batches.id", ondelete="CASCADE"), nullable=False)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())

    # Ensure one student cannot be assigned to the same batch twice
    __table_args__ = (UniqueConstraint("student_id", "batch_id", name="uq_student_batch"),)

    # Optional relationships
    batch = relationship("StudentBatch", back_populates="student_assignments")
