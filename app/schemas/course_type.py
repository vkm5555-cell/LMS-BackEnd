from pydantic import BaseModel
from typing import Optional

class CourseTypeBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: str = "active"

class CourseTypeCreate(CourseTypeBase):
    name: str
    description: str | None = None
    status: str 
    role: str  
    
class CourseTypeOut(CourseTypeBase):
    id: int
    name: str

    class Config:
        from_attributes = True
