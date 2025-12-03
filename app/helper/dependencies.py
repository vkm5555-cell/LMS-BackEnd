# app/dependencies.py
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.db.session import  db as database
from app.models.models import User, Permission, Module
from app.services.auth_service import AuthService  # assumes you have JWT auth

def check_permission(authorization: str, module_name: str, action: str, db: Session):


    if not authorization.startswith("Bearer "):
        return None, JSONResponse(
            status_code=401,
            content={"error_code": 401, "success": False, "message": "Invalid authorization header format"}
        )

    token = authorization.split(" ")[1]
    current_user = db.query(User).filter(User.access_token == token).first()

    if not current_user:
        return None, JSONResponse(
            status_code=401,
            content={"error_code": 300, "success": False, "message": "Invalid token"}
        )
    for role in current_user.roles:
        print(role.id)
    # Iterate through all roles of the user
    for role in current_user.roles:
       
        perm = db.query(Permission).join(Module).filter(
            Permission.role_id == role.id,
            Module.name == module_name
        ).first()
        #print(f"roless Module.name {perm.module.name}")
        if perm and getattr(perm, f"can_{action}", False):
            return True  # Permission granted

    #raise HTTPException(status_code=403, detail="Permission denied")
    return False

def get_current_user(authorization: str, db: Session):
    """
    Extract user from Bearer token in Authorization header
    """
    if not authorization.startswith("Bearer "):
        return None, JSONResponse(
            status_code=401,
            content={"error_code": 401, "success": False, "message": "Invalid authorization header format"}
        )

    token = authorization.split(" ")[1]
    current_user = db.query(User).filter(User.access_token == token).first()

    if not current_user:
        return None, JSONResponse(
            status_code=401,
            content={"error_code": 401, "success": False, "message": "Invalid token"}
        )

    return current_user
    

