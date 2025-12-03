from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DiscussionCommentBase(BaseModel):
    course_id: int
    chapter_id: int
    content_id: int
    discussion_id: int
    user_id: Optional[int] = None
    content: str
    parent_id: Optional[int] = None


class DiscussionCommentCreate(BaseModel):
    user_id: int
    discussion_id: int
    chapter_id: int
    content_id: int
    parent_id: Optional[int] = None
    content: str

class UserOut(BaseModel):
    id: int
    name: Optional[str]
    email: Optional[str]


class DiscussionCommentOut(DiscussionCommentBase):
    id: int
    likes: int
    created_at: datetime
    user: Optional[UserOut]

    class Config:
        from_attributes = True