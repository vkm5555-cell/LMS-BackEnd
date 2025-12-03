from sqlalchemy.orm import Session,joinedload
from fastapi.responses import JSONResponse
from app.models.user_details import UserDetails
from app.schemas.auth import UserCreate, UserUpdate,UserLogin, UserOut, Token, AssignPermissionRequest
from app.services.auth_service import AuthService
from app.services.user_service import UserService

from app.models.models import User, UserRole, Role, Permission
from datetime import datetime

class UserController:

    @staticmethod
    def create(payload: UserCreate, db: Session, authorization: str):
        #print(f'asdfasdf {payload}')
        auth_service = AuthService()
        new_user = auth_service.register(db, payload)

        return JSONResponse(
            content={
                "success": True,
                "message": "User created successfully",
                "data": {
                    "id": new_user.id,
                    "username": new_user.username,
                    "email": new_user.email,

                },
            }
        )

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 10, users=None, total=None):
        if users is None:
            query = db.query(User)
            total = query.count()
            users = query.offset(skip).limit(limit).all()

        return JSONResponse(
            content={
                "success": True,
                "message": "Users retrieved successfully",
                "total": total,
                "skip": skip,
                "limit": limit,
                "data": [
                    {
                        "id": u.id,
                        "name": u.name,
                        "username": u.username,
                        "email": u.email,
                        "mobile": u.mobile,
                        "roles": [role.name for role in u.roles],
                        "dob": u.dob.isoformat() if u.dob else None,
                        "father_name": u.father_name,
                        "mother_name": u.mother_name,
                        "created_at": u.created_at.isoformat() if u.created_at else None,
                        "updated_at": u.updated_at.isoformat() if u.updated_at else None,
                    }
                    for u in users
                ],
            }
        )

    @staticmethod
    def get_by_id(user_id: int, db: Session):
        user = UserService.get_by_id(user_id, db)
        if not user:
            return JSONResponse(
                content={
                    "success": False,
                    "message": f"User with id {user_id} not found",
                },
                status_code=404,
            )
        return JSONResponse(
            content={
                "success": True,
                "message": "User retrieved successfully",
                "data": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role_id": user.role_id,
                },
            }
        )

    @staticmethod
    def update(user_id: int, payload: UserUpdate, db: Session):
        #return user_id
        user = UserService.update(user_id, payload, db)
        #return user
        if not user:
            return JSONResponse(
                content={
                    "success": False,
                    "message": f"User with id {user_id} not found",
                },
                status_code=404,
            )
        return JSONResponse(
            content={
                "success": True,
                "message": "User updated successfully",
                "data": {
                    "id": user_id,
                    "username": user.username,
                    "email": user.email
                },
            }
        )

    @staticmethod
    def delete(user_id: int, db: Session):
        deleted = UserService.delete(user_id, db)
        if not deleted:
            return JSONResponse(
                content={
                    "success": False,
                    "message": f"User with id {user_id} not found",
                },
                status_code=404,
            )
        return JSONResponse(
            content={
                "success": True,
                "message": "User deleted successfully",
            }
        )

    def get_by_id(user_id: int, db: Session):
        permissions = (
            db.query(Permission)
            .join(Role, Role.id == Permission.role_id)
            .join(User.roles)  # user ↔ roles
            .filter(User.id == user_id)
            .options(joinedload(Permission.module))  # eager load module
            .all()
        )
        return permissions

    def get_user_with_permissions(user_id: int, db: Session):
        user_data = UserService.get_user_with_permissions(user_id, db)

        if not user_data:
            return JSONResponse(
                content={"success": False, "message": "User not found"},
                status_code=404
            )

        return JSONResponse(
            content={
                "success": True,
                "message": "User with roles and permissions retrieved successfully",
                "data": user_data
            }
        )

    @staticmethod
    def get_permissions(user_id: int, db: Session):
        permissions = UserService.get_user_permissions(user_id, db)

        if not permissions:
            return JSONResponse(
                content={"success": False, "message": "No permissions found for this user"},
                status_code=404
            )

        return JSONResponse(
            content={
                "success": True,
                "message": "Permissions retrieved successfully",
                "data": [
                    {
                        "id": p.id,
                        "module": {
                            "id": p.module.id if p.module else None,
                            "name": p.module.name if p.module else None,
                            "description": p.module.description if p.module else None,
                        },
                        "can_create": p.can_create,
                        "can_read": p.can_read,
                        "can_update": p.can_update,
                        "can_delete": p.can_delete,
                    }
                    for p in permissions
                ]
            }
        )

    @staticmethod
    def get_permission(permission_id: int, db: Session):
        permission = UserService.get_permission_by_id(permission_id, db)

        if not permission:
            return JSONResponse(
                content={"success": False, "message": "Permission not found"},
                status_code=404
            )

        return JSONResponse(
            content={
                "success": True,
                "message": "Permission retrieved successfully",
                "data": {
                    "id": permission.id,
                    "module": {
                        "id": permission.module.id if permission.module else None,
                        "name": permission.module.name if permission.module else None,
                    },
                    "can_create": permission.can_create,
                    "can_read": permission.can_read,
                    "can_update": permission.can_update,
                    "can_delete": permission.can_delete,
                }
            }
        )

    @staticmethod
    def update_permissions(permission_id: int, permission_flags: list, db):

        try:
            # Fetch permission
            permission = db.query(Permission).filter(Permission.id == permission_id).first()
            if not permission:
                return JSONResponse(
                    content={"success": False, "message": "Permission not found"},
                    status_code=404,
                )

            if len(permission_flags) != 4:
                return JSONResponse(
                    content={
                        "success": False,
                        "message": "Invalid input: permission_flags must be [create, read, update, delete]",
                    },
                    status_code=400,
                )

            # Map values
            permission.can_create = bool(permission_flags[0])
            permission.can_read = bool(permission_flags[1])
            permission.can_update = bool(permission_flags[2])
            permission.can_delete = bool(permission_flags[3])

            db.commit()
            db.refresh(permission)

            return JSONResponse(
                content={
                    "success": True,
                    "message": "Permission updated successfully",
                    "permission": {
                        "id": permission.id,
                        "module_id": permission.module_id,
                        "role_id": permission.role_id,
                        "can_create": permission.can_create,
                        "can_read": permission.can_read,
                        "can_update": permission.can_update,
                        "can_delete": permission.can_delete,
                    },
                },
                status_code=200,
            )

        except Exception as e:
            db.rollback()
            return JSONResponse(
                content={"success": False, "message": str(e)},
                status_code=500,
            )

    @staticmethod
    def get_user_roles(user_id: int, db: Session):
        user_roles = (
            db.query(UserRole, Role)
            .join(Role, Role.id == UserRole.role_id)
            .filter(UserRole.user_id == user_id)
            .all()
        )

        if not user_roles:
            return {
                "success": False,
                "message": f"No roles found for user_id {user_id}"
            }

        roles = [{"role_id": role.id, "role_name": role.name} for (_, role) in user_roles]

        return {
            "success": True,
            "user_id": user_id,
            "roles": roles
        }

    @staticmethod
    def assign_permissions(payload: AssignPermissionRequest, db: Session):
        try:
            permission = UserService.assign_permissions(payload, db)

            return JSONResponse(
                content={
                    "success": True,
                    "message": "Permissions assigned successfully",
                    "data": {
                        "id": permission.id,
                        "role_id": permission.role_id,
                        "module_id": permission.module_id,
                        "can_create": permission.can_create,
                        "can_read": permission.can_read,
                        "can_update": permission.can_update,
                        "can_delete": permission.can_delete,
                    },
                },
                status_code=200,
            )
        except Exception as e:
            db.rollback()
            return JSONResponse(
                content={"success": False, "message": str(e)},
                status_code=500,
            )

    @staticmethod
    def get_user_by_token(authorization: str, db: Session, user_controller=None):
        """
        Get user details using access_token and ensure it's not expired.
        """

        try:
            # Extract the token from the header (Bearer <token>)
            token = authorization.split(" ")[1] if " " in authorization else authorization
            #return token
            # Query the user table for a valid token
            user = (
                db.query(User)
                .join(User.roles)
                .filter(
                    User.access_token.like(f"%{token}%"),
                    User.token_expiry > datetime.utcnow()
                )
                .first()
            )
            #return user
            if not user:
                return None  # token invalid or expired

            # Prepare a clean response dict
            return {
                "id": user.id,
                "name": user.name,
                "username": user.username,
                "email": user.email,
                "roles": [
                    {"id": r.id, "name": r.name}
                    for r in user.roles
                ] if user.roles else [],
                "mobile": user.mobile,
                "dob": str(user.dob) if user.dob else None,
                "father_name": user.father_name,
                "mother_name": user.mother_name,
                "profile_picture": user.profile_picture,
                "token_expiry": user.token_expiry.strftime("%Y-%m-%d %H:%M:%S")
            }

        except Exception as e:
            print(f"Error fetching user by token: {e}")
            return None

    # Get student users
    @staticmethod
    def get_users_by_role(user_role: str, db: Session):
        users = UserService.get_users_by_role(user_role, db)
        return users

    #Store or update user details
    @staticmethod
    def save_or_update_user_details(db, user_id, payload):
        # Check if record exists
        user_details = db.query(UserDetails).filter(UserDetails.user_id == user_id).first()

        if user_details:
            # UPDATE
            user_details.name = payload["name"]
            user_details.email = payload["email"]
            user_details.mobile = payload["mobile"]
            user_details.facebook = payload["facebook"]
            user_details.xcom = payload["xcom"]
            user_details.linkedin = payload["linkedin"]
            user_details.instagram = payload["instagram"]
        else:
            # CREATE
            user_details = UserDetails(
                user_id=user_id,
                name=payload["name"],
                email=payload["email"],
                mobile=payload["mobile"],
                facebook=payload["facebook"],
                xcom=payload["xcom"],
                linkedin=payload["linkedin"],
                instagram=payload["instagram"],
            )
            db.add(user_details)

        db.commit()
        db.refresh(user_details)
        return user_details