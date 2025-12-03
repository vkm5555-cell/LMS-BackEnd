from sqlalchemy import Column, Integer, String, Boolean, DateTime, TIMESTAMP
from app.db.base_class import Base
from datetime import datetime

class StudentCourseProgress(Base):
    __tablename__ = "student_course_content_progress"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, nullable=False)
    course_id = Column(Integer, nullable=False)
    chapter_id = Column(Integer, nullable=False)
    content_id = Column(Integer, nullable=False)
    complete_per = Column(String(50), nullable=False)
    is_completed = Column(Boolean, default=False)
    last_accessed = Column(DateTime, default=datetime.utcnow)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)