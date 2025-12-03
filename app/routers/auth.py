from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import db as database
from app.schemas.auth import UserCreate, UserLogin, UserOut, Token
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["Auth"])
service = AuthService()

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(database.get_db)):
    try:
        created = service.register(db, user)
        return {"id": created.id, "username": created.username, "role": created.role}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(database.get_db)):
    try:
        user, token = service.login(db, payload)
        roles = [r.name for r in user.roles] if user.roles else []
        print(f"asdfdsfsd {roles}")
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role":roles,
                "name": user.name or "",
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
@router.post("/logout")
def logout(username: str, db: Session = Depends(database.get_db)):
    AuthService().logout(db, username)
    return {"message": "User logged out successfully"}        
