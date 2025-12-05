from fastapi import Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.db.session import db as database # <-- FIX: import the actual get_db
from app.schemas.auth import UserCreate, UserLogin
from app.repositories.user_repo import UserRepository
from app.repositories.activity_repo import ActivityRepository
from app.core.security import security
from app.models.models import User
from app.core.config import settings  # SECRET_KEY, ALGORITHM
from app.services.user_service import UserService

# OAuth2 scheme (FastAPI will look for "Authorization: Bearer <token>")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


class AuthService:
    def __init__(
        self,
        repo: UserRepository | None = None,
        activity_repo: ActivityRepository | None = None
    ):
        self.repo = repo or UserRepository()
        self.activity_repo = activity_repo or ActivityRepository()

    def register(self, db: Session, user: UserCreate):

        if self.repo.get_by_username(db, user.username):
            raise ValueError("Username already exists")

        hashed = security.hash_password(user.password)
        #return hashed
        created = self.repo.create(
            db,
            name=user.name,
            username=user.username,
            hashed_password=hashed,
            role=user.role or "Student",
            email=user.email,
            mobile=user.mobile,
            dob=user.dob,
            father_name=user.father_name,
            mother_name=user.mother_name
        )
        return created

    def login(self, db: Session, login: UserLogin) -> tuple[User, str]:
        user = self.repo.get_by_username(db, login.username)
        #return user, user.hashed_password
        if not user or not security.verify_password(login.password, user.hashed_password):
            raise ValueError("Invalid credentials")

        self.activity_repo.create(db, user_id=user.id, action="login")

        token = security.create_access_token(
            subject=user.id,   # use user.id as sub
            role='admin'
        )
        permissions = UserService.get_user_permissions(user.id, db)
        expire = datetime.now(timezone.utc) + timedelta(minutes=90)
        # update user record in DB

        user.access_token = token
        user.token_expiry = expire
        db.add(user)
        db.commit()
        db.refresh(user)
        return user, token
        
    def logout(self, db: Session, username: str):
        user = self.repo.get_by_username(db, username)
        if user:
            self.activity_repo.create(db, user_id=user.id, action="logout")  

    def get_current_user(
        self,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(database.get_db),
    ) -> User:
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )
            user_id: int = payload.get("sub")
            if user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise credentials_exception
        return user

    def get_user_id_from_token(authorization: str = Header(...)) -> int:
        """
        Extract user_id from JWT Authorization header.
        """
        try:
            if not authorization.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="Invalid authorization header")

            token = authorization.split(" ")[1]

            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id: int = payload.get("sub")

            if user_id is None:
                raise HTTPException(status_code=401, detail="Token missing subject (sub)")

            return int(user_id)

        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
