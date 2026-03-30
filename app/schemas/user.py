from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ══════════════════════════════════════════════════════════════════════════════
# Role Schemas
# ══════════════════════════════════════════════════════════════════════════════

class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class RoleCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=255)


class RoleUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=255)


class RoleListResponse(BaseModel):
    total: int
    roles: list[RoleResponse]


# ══════════════════════════════════════════════════════════════════════════════
# UserRole Schemas
# ══════════════════════════════════════════════════════════════════════════════

class UserRoleResponse(BaseModel):
    id: int
    user_id: int
    role_id: int
    assigned_at: datetime
    role: RoleResponse

    class Config:
        from_attributes = True


class AssignRoleRequest(BaseModel):
    role_id: int = Field(..., gt=0)


# ══════════════════════════════════════════════════════════════════════════════
# User Schemas
# ══════════════════════════════════════════════════════════════════════════════

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    provider: str
    is_active: bool
    is_verified: bool
    last_login_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    roles: list[UserRoleResponse] = []

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    users: list[UserResponse]


class UserUpdateRequest(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None