from sqlalchemy import Column, BigInteger, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base  # Make sure Base is imported

class Discussion(Base):
    __tablename__ = 'discussions'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    course_id = Column(BigInteger, nullable=False)
    chapter_id = Column(BigInteger, nullable=False)
    content_id = Column(BigInteger, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    likes = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP', onupdate='CURRENT_TIMESTAMP')

    relationship("DiscussionComment")
