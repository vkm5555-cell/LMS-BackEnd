from sqlalchemy import Column, Integer, String, DateTime, func
from app.models.base import Base


class SessionModel(Base):
    __tablename__ = "session"

    id = Column(Integer, primary_key=True, index=True)
    session = Column(String(255))
    status = Column(String(10))
    is_deleted = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())