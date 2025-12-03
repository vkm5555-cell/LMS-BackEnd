from sqlalchemy import Column, Integer, String, ForeignKey, Table, Date, DateTime, Boolean, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

# enrollments = Table(
#     "enrollments", Base.metadata,
#     Column("student_id", Integer, ForeignKey("students.id", ondelete="CASCADE"), primary_key=True),
#     Column("course_id", Integer, ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True),
# )

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="student")

    # New fields
    email = Column(String, unique=True, nullable=False)
    mobile = Column(String, nullable=False)
    dob = Column(Date, nullable=True)
    father_name = Column(String, nullable=True)
    mother_name = Column(String, nullable=True)

    access_token = Column(String, nullable=True)
    token_expiry = Column(DateTime, nullable=True)
    profile_picture = Column(String, nullable=True)
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    activities = relationship("ActivityLog", back_populates="user")

    roles = relationship("Role", secondary="user_roles", back_populates="users")
    courses = relationship("Course", back_populates="user")

    chapters = relationship("CourseChapter", back_populates="user", cascade="all, delete-orphan")
    batches = relationship("StudentBatch", back_populates="user")
    #details = relationship("UserDetails", uselist=False, back_populates="user", cascade="all, delete-orphan")



class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))

    users = relationship("User", secondary="user_roles", back_populates="roles")
    permissions = relationship("Permission", back_populates="role")


class UserRole(Base):
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"))
    UniqueConstraint("user_id", "role_id", name="uq_user_role")   


class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))
    status = Column(String(50), default="active")

    permissions = relationship("Permission", back_populates="module")    


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"), nullable=False)
    can_create = Column(Boolean, default=False)
    can_read = Column(Boolean, default=True)
    can_update = Column(Boolean, default=False)
    can_delete = Column(Boolean, default=False)

    role = relationship("Role", back_populates="permissions")
    module = relationship("Module", back_populates="permissions")         


# class Student(Base):
#     __tablename__ = "students"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(100), nullable=False)
#     email = Column(String(100), unique=True, index=True)
#     courses = relationship("Course", secondary=enrollments, back_populates="students")
#
# class Course(Base):
#     __tablename__ = "courses"
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(200), nullable=False)
#     description = Column(String(500))
#     students = relationship("Student", secondary=enrollments, back_populates="courses")
    
class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(50))  
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="activities")    
