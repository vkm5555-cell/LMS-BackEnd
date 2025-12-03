from sqlalchemy.orm import Session
from app.models.discussions import Discussion
from app.models.discussion_comments import DiscussionComment
from app.schemas.discussions import DiscussionCreate
from app.schemas.discussion_comments import DiscussionCommentCreate
from app.models.course_chapter import CourseChapter
from app.models.models import User


class DiscussionService:

    # ---------------------------------------------------------
    # CREATE DISCUSSION
    # ---------------------------------------------------------
    @staticmethod
    def create_discussion(db: Session, payload: DiscussionCreate):

        course_id = DiscussionService.get_course_id_by_chapter(db, payload.chapter_id)

        if not course_id:
            raise ValueError("Invalid chapter_id. Course not found.")

        discussion = Discussion(
            course_id=course_id,
            chapter_id=payload.chapter_id,
            content_id=payload.content_id,
            user_id=payload.user_id,
            title=payload.title,
            content=payload.content
        )

        db.add(discussion)
        db.commit()
        db.refresh(discussion)

        return discussion

    # ---------------------------------------------------------
    # GET COURSE ID BY CHAPTER ID
    # ---------------------------------------------------------
    @staticmethod
    def get_course_id_by_chapter(db: Session, chapter_id: int):
        chapter = db.query(CourseChapter).filter(CourseChapter.id == chapter_id).first()
        return chapter.course_id if chapter else None

    # ---------------------------------------------------------
    # GET DISCUSSIONS BY CONTENT ID + USER DETAIL
    # ---------------------------------------------------------
    @staticmethod
    def get_discussions_by_content_id(db: Session, content_id: int):

        discussions = (
            db.query(Discussion)
            .filter(Discussion.content_id == content_id)
            .order_by(Discussion.created_at.desc())
            .all()
        )

        result = []
        for d in discussions:
            user = db.query(User).filter(User.id == d.user_id).first()

            user_data = None
            if user:
                user_data = {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email
                }

            # Fetch nested comments for each discussion
            comments = DiscussionService.get_comments_by_discussion(db, d.id)

            result.append({
                "id": d.id,
                "course_id": d.course_id,
                "chapter_id": d.chapter_id,
                "content_id": d.content_id,
                "title": d.title,
                "content": d.content,
                "likes": d.likes,
                "created_at": d.created_at,
                "updated_at": d.updated_at,
                "user": user_data,
                "user_id": d.user_id,
                "comments": comments,
            })

        return result

    # ---------------------------------------------------------
    # CREATE COMMENT (TOP LEVEL OR REPLY)
    # ---------------------------------------------------------
    @staticmethod
    def create_comment(db: Session, user_id: int, payload: DiscussionCommentCreate):
        course_id = DiscussionService.get_course_id_by_chapter(db, payload.chapter_id)
        comment = DiscussionComment(
            course_id=course_id,
            chapter_id=payload.chapter_id,
            content_id=payload.content_id,
            discussion_id=payload.discussion_id,
            user_id=user_id,
            parent_id=payload.parent_id,
            content=payload.content
        )

        db.add(comment)
        db.commit()
        db.refresh(comment)

        return comment

    # ---------------------------------------------------------
    # GET COMMENTS (NESTED)
    # ---------------------------------------------------------
    @staticmethod
    def get_comments_by_discussion(db: Session, discussion_id: int):
        comments = (
            db.query(DiscussionComment)
            .filter(DiscussionComment.discussion_id == discussion_id)
            .order_by(DiscussionComment.created_at.asc())
            .all()
        )

        results = []

        for c in comments:
            # fetch user info
            user = db.query(User).filter(User.id == c.user_id).first()

            results.append({
                "id": c.id,
                "discussion_id": c.discussion_id,
                "course_id": c.course_id,
                "chapter_id": c.chapter_id,
                "content_id": c.content_id,
                "user_id": c.user_id,
                "parent_id": c.parent_id,
                "content": c.content,
                "likes": c.likes,
                "created_at": c.created_at,
                "replies": [],

                # ALWAYS INCLUDE THIS KEY
                "user": {
                    "id": user.id if user else None,
                    "name": getattr(user, "name", None) if user else None,
                    "email": getattr(user, "email", None) if user else None,
                    "avatar": getattr(user, "avatar", None) if user else None,
                }
            })

        return results

    @staticmethod
    def attach_replies(tree_node, comment_obj):
        if tree_node["id"] == comment_obj.id and hasattr(comment_obj, "children"):
            tree_node["replies"] = comment_obj.children
        else:
            for child in tree_node["replies"]:
                DiscussionService.attach_replies(child, comment_obj)
