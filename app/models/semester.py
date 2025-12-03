from sqlalchemy import Column, Integer, String, DateTime, func
from app.models.base import Base

class Semester(Base):
    __tablename__ = "semester"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    code = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
