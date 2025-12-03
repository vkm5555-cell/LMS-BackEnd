# app/schemas/course_category.py
from typing import Optional, List
from pydantic import BaseModel


# Shared properties
class CourseCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    keyword: Optional[str] = None
    parent_category_id: int = 0


class CourseCategoryOut(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        from_attributes = True


# Create schema (input)
class CourseCategoryCreate(CourseCategoryBase):
    name: str
    description: Optional[str] = None
    keyword: Optional[str] = None
    parent_category_id: Optional[int] = None


# Update schema (input)
class CourseCategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    keyword: Optional[str] = None
    parent_category_id: Optional[int] = None


# Output schema (DB -> API response)
class CourseCategoryInDBBase(CourseCategoryBase):
    id: int

    class Config:
        from_attributes = True  # allows ORM -> Pydantic conversion


# For API response (without children)
class CourseCategory(CourseCategoryInDBBase):
    pass


# For API response with nested children
class CourseCategoryWithChildren(CourseCategoryInDBBase):
    children: List["CourseCategoryWithChildren"] = []


# Fix forward references for self-referencing children
CourseCategoryWithChildren.model_rebuild()

class PaginatedCourseCategory(BaseModel):
    data: List[CourseCategory]
    page: int
    page_size: int
    total: int
    total_pages: int
