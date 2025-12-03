# app/services/course_category_service.py
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.models.course_category import CourseCategory
from app.schemas.course_category import (
    CourseCategoryCreate,
    CourseCategoryUpdate
)
from sqlalchemy import or_

# Create a new category
def create_category(db: Session, payload: CourseCategoryCreate):
    parent_id = payload.parent_category_id if payload.parent_category_id is not None else 0
    category = CourseCategory(
        name=payload.name,
        description=payload.description,
        keyword=payload.keyword,
        parent_category_id=parent_id
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

# Get category by ID
def get_category(db: Session, category_id: int) -> Optional[CourseCategory]:
    return db.query(CourseCategory).filter(CourseCategory.id == category_id).first()


# Get categories with pagination
def get_categories(db, skip: int = 0, limit: int = 10, search=None):
    # Build query
    query = db.query(CourseCategory)
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                CourseCategory.name.ilike(search_pattern)
            )
        )

    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": items,
    }


# Update category
def update_category(
    db: Session, category_id: int, category_in: CourseCategoryUpdate
) -> Optional[CourseCategory]:
    category = get_category(db, category_id)
    if not category:
        return None
    
    update_data = category_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "parent_category_id" and value is None:  # if NULL
            setattr(category, field, 0)  # set 0 instead
        else:
            setattr(category, field, value)

    db.commit()
    db.refresh(category)
    return category


# Delete category
def delete_category(db: Session, category_id: int) -> bool:
    category = get_category(db, category_id)
    if not category:
        return False
    
    db.delete(category)
    db.commit()
    return True
