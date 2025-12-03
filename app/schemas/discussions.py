from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .discussion_comments import DiscussionCommentOut  # import comment schema


class DiscussionBase(BaseModel):
    course_id: int
    chapter_id: int
    content_id: int
    user_id: int
    title: Optional[str] = None
    content: str

class UserOut(BaseModel):
    id: int
    name: Optional[str]
    email: Optional[str]


class DiscussionCreate(DiscussionBase):
    pass


class DiscussionOut(DiscussionBase):
    id: int
    likes: int
    created_at: datetime
    updated_at: datetime
    comments: List[DiscussionCommentOut] = []
    user: Optional[UserOut]

    class Config:
        from_attributes = True