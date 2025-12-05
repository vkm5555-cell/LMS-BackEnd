from sqlalchemy.orm import Session, joinedload
from app.models.models import User, UserRole, Role, Permission
from app.schemas.auth import UserCreate, UserUpdate, UserLogin, UserOut, Token, AssignPermissionRequest
from app.core.security import security


class UserService:

    @staticmethod
    def list(db: Session):
        return db.query(User).all()

    @staticmethod
    def get_by_id(user_id: int, db: Session):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def create(payload: UserCreate, db: Session):
        hashed_password = security.hash_password(payload.password)

        new_user = User(
            name=payload.name,
            username=payload.username,
            hashed_password=hashed_password,
            email=payload.email,
            mobile=payload.mobile,
            dob=payload.dob,
            father_name=payload.father_name,
            mother_name=payload.mother_name,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        user_role = UserRole(user_id=new_user.id, role_id=payload.role_id)
        db.add(user_role)
        db.commit()

        return new_user

    @staticmethod
    def update(user_id: int, payload: UserUpdate, db: Session):
        #return user_id
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None

        if payload.name is not None:
            user.name = payload.name
        if payload.email is not None:
            user.email = payload.email
        if payload.mobile is not None:
            user.mobile = payload.mobile
        if payload.dob is not None:
            user.dob = payload.dob
        if payload.father_name is not None:
            user.father_name = payload.father_name
        if payload.mother_name is not None:
            user.mother_name = payload.mother_name
        if payload.password not in (None, ""):
            user.hashed_password = security.hash_password(payload.password)

        db.commit()
        db.refresh(user)

        if payload.role_id is not None:
            # clear existing roles
            db.query(UserRole).filter(UserRole.user_id == user_id).delete()

            # assign new roles
            for r_id in payload.role_id:
                new_role = UserRole(user_id=user.id, role_id=r_id)
                db.add(new_role)
            db.commit()
        #user = db.query(User).filter(User.id == user_id).first()
        return user

    @staticmethod
    def delete(user_id: int, db: Session):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False

        # Delete user roles first
        db.query(UserRole).filter(UserRole.user_id == user.id).delete()

        db.delete(user)
        db.commit()
        return True

    @staticmethod
    def get_by_id(user_id: int, db: Session):
        user = (
            db.query(User)
            .options(
                joinedload(User.roles)  # eager load roles
                .joinedload(Role.permissions)  # eager load permissions
                .joinedload(Permission.module)  # eager load module
            )
            .filter(User.id == user_id)
            .first()
        )
        return user

    def get_user_permissions(user_id: int, db: Session):
        permissions = (
            db.query(Permission)
            .join(Permission.role)  # join via relationship
            .join(Role.users)  # join user through roles
            .filter(User.id == user_id)
            .options(joinedload(Permission.module))
            .all()
        )

        return permissions

    def get_permission_by_id(permission_id: int, db: Session):
        permission = (
            db.query(Permission)
            .options(joinedload(Permission.module))  # eager load module
            .filter(Permission.id == permission_id)
            .first()
        )
        return permission

    @staticmethod
    def get_user_with_permissions(user_id: int, db: Session):
        """
        Fetch user details with roles, permissions, and modules.
        """
        user = (
            db.query(User)
            .filter(User.id == user_id)
            .options(
                joinedload(User.roles)
                .joinedload(Role.permissions)
                .joinedload(Permission.module)
            )
            .first()
        )

        if not user:
            return None

        # Build structured response
        user_details = {
            "id": user.id,
            "name": user.name,
            "username": user.username,
            "email": user.email,
            "mobile": user.mobile,
            "dob": str(user.dob) if user.dob else None,
            "father_name": user.father_name,
            "mother_name": user.mother_name,
            "created_at": str(user.created_at) if user.created_at else None,
            "updated_at": str(user.updated_at) if user.updated_at else None,
            "roles": [],
            "permissions": []
        }

        roles_set = set()
        for role in user.roles:
            # collect roles
            if role.id not in roles_set:
                user_details["roles"].append({
                    "id": role.id,
                    "name": role.name
                })
                roles_set.add(role.id)

            # collect permissions for each role
            for perm in role.permissions:
                user_details["permissions"].append({
                    "id": perm.id,
                    "module": {
                        "id": perm.module.id if perm.module else None,
                        "name": perm.module.name if perm.module else None,
                        "description": perm.module.description if perm.module else None,
                    },
                    "can_create": perm.can_create,
                    "can_read": perm.can_read,
                    "can_update": perm.can_update,
                    "can_delete": perm.can_delete,
                })

        return user_details

    @staticmethod
    def assign_permissions(payload: AssignPermissionRequest, db: Session) -> Permission:
        """
        Assign or update permissions for a role on a module.
        Returns the Permission object after save/update.
        """

        # Convert permission_ids list [1,0,0,1] -> booleans
        can_create, can_read, can_update, can_delete = [
            bool(x) for x in payload.permission_ids
        ]

        permission = (
            db.query(Permission)
            .filter(
                Permission.role_id == payload.role_id,
                Permission.module_id == payload.module_id
            )
            .first()
        )

        if permission:
            # Update existing
            permission.can_create = can_create
            permission.can_read = can_read
            permission.can_update = can_update
            permission.can_delete = can_delete
        else:
            # Create new
            permission = Permission(
                role_id=payload.role_id,
                module_id=payload.module_id,
                can_create=can_create,
                can_read=can_read,
                can_update=can_update,
                can_delete=can_delete,
            )
            db.add(permission)

        db.commit()
        db.refresh(permission)
        return permission


    @staticmethod
    def get_users_by_role(role_name: str, db: Session):
        return (
            db.query(User)
            .join(UserRole)
            .join(Role)
            .filter(Role.name == role_name)
            .all()
        )

