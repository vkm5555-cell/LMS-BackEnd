# app/schemas/course.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CourseCreate(BaseModel):
    title: str
    slug: str
    course_type: str = "free"
    category_id: int
    course_price: float = 0.0
    course_mode: str = "online"
    cafeteria: Optional[str] = None
    nsqf_level: Optional[str] = None
    credit: Optional[str] = None
    course_time: Optional[str] = None
    description: Optional[str] = None
    subtitle: Optional[str] = None
    learning_objectives: Optional[str] = None
    requirements: Optional[str] = None
    language: Optional[str] = "English"
    level: Optional[str] = "Beginner"
    topic_tags: Optional[str] = None
    course_thumb: Optional[str] = None
    promo_video_url: Optional[str] = None
    user_id: Optional[int] = None


class CourseOut(BaseModel):
    id: int
    title: str
    slug: str
    course_type: str
    category_id: int
    course_price: float
    course_mode: str
    cafeteria: Optional[str] = None
    nsqf_level: Optional[str] = None
    credit: Optional[str] = None
    course_time: Optional[str] = None
    description: Optional[str] = None
    subtitle: Optional[str] = None
    learning_objectives: Optional[str] = None
    requirements: Optional[str] = None
    language: str
    level: str
    topic_tags: Optional[str] = None
    course_thumb: Optional[str] = None
    promo_video_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    user_id: Optional[int] = None

    class Config:
        from_attributes = True