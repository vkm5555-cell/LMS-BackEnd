from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CourseAssignmentBase(BaseModel):
    user_id: Optional[int]
    course_id: int
    title: str
    description: Optional[str] = None
    file_path: Optional[str] = None
    max_marks: Optional[int] = 100
    due_date: Optional[datetime] = None


class CourseAssignmentCreate(CourseAssignmentBase):
    pass


class CourseAssignmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    file_path: Optional[str] = None
    max_marks: Optional[int] = None
    due_date: Optional[datetime] = None


class CourseAssignmentOut(CourseAssignmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True