from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Literal

class StudentBatchBase(BaseModel):
    name: str
    description: Optional[str] = None
    organization_id: int
    session_id: str
    semester_id: str
    course_id: int
    start_date: datetime
    end_date: datetime
    status: Optional[Literal["active", "inactive"]] = "active"

class StudentBatchCreate(StudentBatchBase):
    user_id: Optional[int] = None

class StudentBatchResponse(StudentBatchBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
