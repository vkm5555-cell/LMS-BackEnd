from sqlalchemy.orm import Session
from .base import BaseRepository
from app.models.models import User
from datetime import date

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_id(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()    

    def get_by_username(self, db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    def get_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def create(
        self,
        db: Session,
        name: str,
        username: str,
        hashed_password: str,
        role: str,
        email: str,
        mobile: str,
        dob: str,
        father_name: str,
        mother_name: str,
    ):
        db_user = User(
            name=name,
            username=username,
            hashed_password=hashed_password,
            role=role,
            email=email,
            mobile=mobile,
            dob=dob,
            father_name=father_name,
            mother_name=mother_name,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

