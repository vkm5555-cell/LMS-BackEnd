# app/models/course_category.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class CourseCategory(Base):
    __tablename__ = "course_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)  # Category description
    keyword = Column(Text, nullable=True)  # SEO or search keywords

    parent_category_id = Column(Integer, ForeignKey("course_categories.id"), nullable=True)

    parent = relationship("CourseCategory", remote_side=[id], backref="subcategories")

    # back_populates with Course
    courses = relationship("Course", back_populates="category")
