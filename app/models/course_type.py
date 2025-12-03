from sqlalchemy import Column, Integer, String, Text
from .base import Base

class CourseType(Base):
    __tablename__ = "course_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="active")
