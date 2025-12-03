from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import List, Optional


class UserCreate(BaseModel):
    id: Optional[int] = None
    name: str
    username: str
    password: str
    role: Optional[str] = "Student"
    role_id: Optional[int] = None
    email: EmailStr
    mobile: str
    dob: datetime
    father_name: Optional[str]
    mother_name: Optional[str]


class UserUpdate(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    email: Optional[EmailStr] = None
    mobile: Optional[str] = None
    dob: datetime   = None
    father_name: Optional[str] = None
    mother_name: Optional[str] = None
    role_id: Optional[List[int]] = None



class UserOut(BaseModel):
    id: int
    name: str
    username: str
    role: list[str] = []

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut


class ModuleBase(BaseModel):
    name: str
    description: Optional[str]


class ModuleCreate(ModuleBase):
    pass


class RoleBase(BaseModel):
    name: str
    description: Optional[str]


class RoleCreate(RoleBase):
    pass


class PermissionBase(BaseModel):
    role_id: int
    module_id: int
    can_create: bool = False
    can_read: bool = True
    can_update: bool = False
    can_delete: bool = False


class PermissionCreate(PermissionBase):
    pass


class UserRoleAssign(BaseModel):
    user_id: int
    role_ids: List[int]

class UpdateUserPermissionsRequest(BaseModel):
    permission_ids: List[int]


class AssignPermissionRequest(BaseModel):
    role_id: int
    module_id: int
    user_id: int
    permission_ids: List[int]
