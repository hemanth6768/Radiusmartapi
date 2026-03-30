from fastapi import APIRouter, Depends, Query, status
from typing import List
from app.dependencies.user_dependency import (
    get_user_service,
    get_role_service,
    get_user_role_service,
)
from app.Service.user_service import UserService, RoleService, UserRoleService
from app.schemas.user import (
    UserResponse,
    UserListResponse,
    UserUpdateRequest,
    RoleResponse,
    RoleListResponse,
    RoleCreateRequest,
    RoleUpdateRequest,
    UserRoleResponse,
    AssignRoleRequest,
)
from app.dependencies.auth_dependency import get_current_user, require_role

router = APIRouter(tags=["Users & Roles"])


# ══════════════════════════════════════════════════════════════════════════════
# User Endpoints  →  /users
# ══════════════════════════════════════════════════════════════════════════════

@router.get(
    "/users",
    response_model=UserListResponse,
    summary="List all users",
    description="Admin only. Returns a paginated list of every user.",
)
def list_users(
    _: dict = Depends(require_role("Admin")),
    service: UserService = Depends(get_user_service),
    skip: int = 0,
    limit: int = 10
):
    return service.get_all_users(skip, limit)

@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
)
def get_user(
    user_id: int,
    current_user: dict = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    return service.get_user_by_id(user_id)


@router.patch(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="Update user",
    description="Users can update their own profile. Admins can update any user.",
)
def update_user(
    user_id: int,
    payload: UserUpdateRequest,
    current_user: dict = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    return service.update_user(user_id, payload, current_user)


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description="Users can delete their own account. Admins can delete any account.",
)
def delete_user(
    user_id: int,
    current_user: dict = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    service.delete_user(user_id, current_user)


# ══════════════════════════════════════════════════════════════════════════════
# Role Endpoints  →  /roles
# ══════════════════════════════════════════════════════════════════════════════

@router.get(
    "/roles",
    response_model=RoleListResponse,
    summary="List all roles",
    description="Admin only. Returns all available roles.",
)
def list_roles(
    _: dict = Depends(require_role("Admin")),
    service: RoleService = Depends(get_role_service),
):
    return service.get_all_roles()


@router.get(
    "/roles/{role_id}",
    response_model=RoleResponse,
    summary="Get role by ID",
)
def get_role(
    role_id: int,
    _: dict = Depends(require_role("Admin")),
    service: RoleService = Depends(get_role_service),
):
    return service.get_role_by_id(role_id)


@router.post(
    "/roles",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new role",
)
def create_role(
    payload: RoleCreateRequest,
    _: dict = Depends(require_role("Admin")),
    service: RoleService = Depends(get_role_service),
):
    return service.create_role(payload)


@router.patch(
    "/roles/{role_id}",
    response_model=RoleResponse,
    summary="Update a role",
)
def update_role(
    role_id: int,
    payload: RoleUpdateRequest,
    _: dict = Depends(require_role("Admin")),
    service: RoleService = Depends(get_role_service),
):
    return service.update_role(role_id, payload)


@router.delete(
    "/roles/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a role",
)
def delete_role(
    role_id: int,
    _: dict = Depends(require_role("Admin")),
    service: RoleService = Depends(get_role_service),
):
    service.delete_role(role_id)


# ══════════════════════════════════════════════════════════════════════════════
# User-Role Endpoints  →  /users/{user_id}/roles
# ══════════════════════════════════════════════════════════════════════════════

@router.get(
    "/users/{user_id}/roles",
    response_model=list[UserRoleResponse],
    summary="Get roles assigned to a user",
)
def get_user_roles(
    user_id: int,
    _: dict = Depends(require_role("Admin")),
    service: UserRoleService = Depends(get_user_role_service),
):
    return service.get_user_roles(user_id)


@router.post(
    "/users/{user_id}/roles",
    response_model=UserRoleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Assign a role to a user",
)
def assign_role(
    user_id: int,
    payload: AssignRoleRequest,
    _: dict = Depends(require_role("Admin")),
    service: UserRoleService = Depends(get_user_role_service),
):
    return service.assign_role(user_id, payload.role_id)


@router.delete(
    "/users/{user_id}/roles/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Revoke a role from a user",
)
def revoke_role(
    user_id: int,
    role_id: int,
    _: dict = Depends(require_role("Admin")),
    service: UserRoleService = Depends(get_user_role_service),
):
    service.revoke_role(user_id, role_id)