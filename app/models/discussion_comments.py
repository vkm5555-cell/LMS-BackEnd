from sqlalchemy import Column, BigInteger, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base  # Make sure Base is imported

class DiscussionComment(Base):
    __tablename__ = 'discussion_comments'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    course_id = Column(BigInteger, nullable=False)
    chapter_id = Column(BigInteger, nullable=False)
    content_id = Column(BigInteger, nullable=False)
    discussion_id = Column(BigInteger, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    parent_id = Column(BigInteger, nullable=True)
    content = Column(Text, nullable=False)
    likes = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')

    relationship("Discussion")
    #replies = relationship('DiscussionComment', cascade='all, delete')
