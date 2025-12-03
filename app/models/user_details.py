from sqlalchemy import Column, Integer, String, Date, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class UserDetails(Base):
    __tablename__ = "user_details"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=True)

    profile_image = Column(String(255), nullable=True)
    profile_image_thumb = Column(String(255), nullable=True)

    dob = Column(Date, nullable=True)
    father_name = Column(String(255), nullable=True)
    mother_name = Column(String(255), nullable=True)
    gender = Column(String(20), nullable=True)
    marital_status = Column(String(50), nullable=True)

    permanent_address_line1 = Column(String(255), nullable=True)
    permanent_address_line2 = Column(String(255), nullable=True)
    permanent_city = Column(String(100), nullable=True)
    permanent_state = Column(String(100), nullable=True)
    permanent_country = Column(String(100), nullable=True)
    permanent_pincode = Column(String(20), nullable=True)

    current_address_line1 = Column(String(255), nullable=True)
    current_address_line2 = Column(String(255), nullable=True)
    current_city = Column(String(100), nullable=True)
    current_state = Column(String(100), nullable=True)
    current_country = Column(String(100), nullable=True)
    current_pincode = Column(String(20), nullable=True)

    bio = Column(Text, nullable=True)
    facebook = Column(String(100), nullable=True)
    x_com = Column(String(100), nullable=True)
    linkedin = Column(String(100), nullable=True)
    instagram = Column(String(100), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)

    #user = relationship("User", back_populates="user_details")
