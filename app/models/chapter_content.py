from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Enum, JSON, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.db.session import Base
from sqlalchemy.dialects.mysql import LONGTEXT

class ContentTypeEnum(enum.Enum):
    video = "video"
    pdf = "pdf"
    text = "text"
    quiz = "quiz"
    assignment = "assignment"
    interactive = "interactive"

class ChapterContent(Base):
    __tablename__ = "chapter_contents"

    id = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=True)
    slug = Column(String(255), nullable=True)
    description = Column(Text, nullable=False)
    content_type = Column(Text, nullable=False)
    content_url = Column(Text, nullable=False)
    content = Column(LONGTEXT, nullable=False)
    video_duration = Column(Integer, nullable=False)
    position = Column(Integer, nullable=False)
    is_published = Column(Boolean, nullable=False, default=False)
    is_free = Column(Boolean, nullable=False, default=False)
    thumbnail_url = Column(Text, nullable=False)
    meta_data = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships (optional)

    #user = relationship("User", back_populates="uploaded_contents")

