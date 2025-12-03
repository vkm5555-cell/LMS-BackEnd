from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ChapterItem(BaseModel):
    title: str
    description: Optional[str] = None
    order: int


class CourseChaptersCreate(BaseModel):
    course_id: int
    chapters: List[ChapterItem]


class CourseChapterResponse(BaseModel):
    id: int
    course_id: int
    user_id: Optional[int]
    chapter_name: str
    description: Optional[str]
    order: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
