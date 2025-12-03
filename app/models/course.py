# app/models/course.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Numeric, func
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship
from app.models.base import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    cafeteria = Column(String(200), nullable=True)
    nsqf_level = Column(String(200), nullable=True)
    credit = Column(String(200), nullable=True)
    course_time = Column(String(200), nullable=True)
    description = Column(String(500), nullable=True)
    subtitle = Column(String(255), nullable=True)
    slug = Column(String(255), nullable=False, unique=True)
    learning_objectives = Column(Text, nullable=True)
    requirements = Column(Text, nullable=True)
    language = Column(String(50), nullable=False, server_default='English')
    level = Column(String(50), nullable=False, server_default='Beginner')
    topic_tags = Column(JSON, nullable=True)
    course_thumb = Column(String(255), nullable=True)
    promo_video_url = Column(String(255), nullable=True)

    # new fields
    course_type = Column(String(50), nullable=False, server_default="free")
    course_mode = Column(String(50), nullable=True)
    course_price = Column(Numeric(10, 2), nullable=True)

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="courses")

    category_id = Column(Integer, ForeignKey("course_categories.id"), nullable=True)
    category = relationship("CourseCategory", back_populates="courses")  # notice string here

    user = relationship("User", back_populates="courses")

    chapters = relationship("CourseChapter", back_populates="course", cascade="all, delete-orphan")
