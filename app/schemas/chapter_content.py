from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class ChapterContentBase(BaseModel):
    chapter_id: int
    user_id: int
    title: Optional[str]
    slug: Optional[str]
    description: Optional[str]
    content_type: Optional[str]
    content_url: Optional[str]
    content: Optional[str]
    video_duration: Optional[int]
    position: Optional[int]
    is_published: Optional[bool] = False
    is_free: Optional[bool] = True
    thumbnail_url: Optional[str]
    meta_data: Optional[Any]

class ChapterContentCreate(BaseModel):
    user_id: int
    title: str


class ChapterContentResponse(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
