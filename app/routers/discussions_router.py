from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.db.session import db as database
from app.schemas.discussions import DiscussionCreate, DiscussionOut
from app.schemas.discussion_comments import DiscussionCommentCreate, DiscussionCommentOut
from app.controllers.discussions_controller import DiscussionService
from app.db.session import db as database
from app.models.models import User, UserRole, Role, Permission

router = APIRouter(prefix="/discussions", tags=["Discussions"])


@router.post("/", response_model=DiscussionOut)
def create_discussion(payload: DiscussionCreate, db: Session = Depends(database.get_db)):
    discussion = DiscussionService.create_discussion(db, payload)
    user = db.query(User).filter(User.id == discussion.user_id).first()

    return {
        "id": discussion.id,
        "course_id": discussion.course_id,
        "chapter_id": discussion.chapter_id,
        "content_id": discussion.content_id,
        "user_id": discussion.user_id,
        "title": discussion.title,
        "content": discussion.content,
        "likes": discussion.likes,
        "created_at": discussion.created_at,
        "updated_at": discussion.updated_at,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        } if user else None
    }


#Get discussions by content_id
@router.get("/", response_model=list[DiscussionOut])
def get_discussions_by_content_id(
    content_id: int = Query(..., description="ID of chapter_content"),
    db: Session = Depends(database.get_db)
):
    return DiscussionService.get_discussions_by_content_id(db, content_id)


# ---------------------------------------------------------
# CREATE DISCUSSION COMMENT / REPLY
# ---------------------------------------------------------
@router.post("/comment", response_model=DiscussionCommentOut)
def create_comment(
    payload: DiscussionCommentCreate,
    db: Session = Depends(database.get_db)
):
    # Validate user_id
    if not payload.user_id or payload.user_id == "":
        raise HTTPException(status_code=400, detail="user_id is required")

    # Create comment
    comment = DiscussionService.create_comment(db, payload.user_id, payload)

    # Fetch user details
    user = db.query(User).filter(User.id == comment.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Return correct structure matching Pydantic model
    return {
        "id": int(comment.id),
        "discussion_id": int(comment.discussion_id),
        "course_id": int(comment.course_id),
        "chapter_id": int(comment.chapter_id),
        "content_id": int(comment.content_id),
        "user_id": int(comment.user_id),
        "parent_id": int(comment.parent_id) if comment.parent_id else None,
        "content": comment.content,
        "likes": int(comment.likes),
        "created_at": comment.created_at,
        "replies": [],  # always include this
        "user": {
            "id": int(user.id),
            "name": user.name,
            "email": user.email,
            "avatar": getattr(user, "avatar", None)
        }
    }



# ---------------------------------------------------------
# GET ALL COMMENTS (NESTED)
# ---------------------------------------------------------
@router.get("/{discussion_id}/comments")
def get_comments(discussion_id: int, db: Session = Depends(database.get_db)):
    return DiscussionService.get_comments_by_discussion(db, discussion_id)
