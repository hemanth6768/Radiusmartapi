from pydantic import BaseModel, EmailStr
from typing import Optional


class SignupRequest(BaseModel):

    email: EmailStr
    password: str
    first_name: Optional[str]
    last_name: Optional[str]


class LoginRequest(BaseModel):

    email: EmailStr
    password: str


class RoleCreate(BaseModel):

    name: str
    description: Optional[str]


class PermissionCreate(BaseModel):

    name: str
    description: Optional[str]


class AssignRoleRequest(BaseModel):

    user_id: int
    role_id: int


class AssignPermissionRequest(BaseModel):

    role_id: int
    permission_id: int


class TokenResponse(BaseModel):

    access_token: str
    token_type: str = "bearer"