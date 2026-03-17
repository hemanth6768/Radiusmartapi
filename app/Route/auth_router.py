# app/api/routes/auth.py

from fastapi import APIRouter, Depends
from app.schemas.auth import (
    SignupRequest, LoginRequest, TokenResponse,
    RoleCreate, PermissionCreate,
    AssignRoleRequest, AssignPermissionRequest
)

from app.Service.auth_service import AuthService
from app.dependencies.auth_dependency import get_auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
def signup(
    request: SignupRequest,
    service: AuthService = Depends(get_auth_service)
):
    user = service.signup(request)
    return {"message": "User created", "user_id": user.id}


@router.post("/login", response_model=TokenResponse)
def login(
    request: LoginRequest,
    service: AuthService = Depends(get_auth_service)
):
    token = service.login(request)
    return {"access_token": token}


@router.post("/roles")
def create_role(
    request: RoleCreate,
    service: AuthService = Depends(get_auth_service)
):
    return service.create_role(request)


@router.post("/permissions")
def create_permission(
    request: PermissionCreate,
    service: AuthService = Depends(get_auth_service)
):
    return service.create_permission(request)


@router.post("/assign-role")
def assign_role(
    request: AssignRoleRequest,
    service: AuthService = Depends(get_auth_service)
):
    return service.assign_role(request)


@router.post("/assign-permission")
def assign_permission(
    request: AssignPermissionRequest,
    service: AuthService = Depends(get_auth_service)
):
    return service.assign_permission(request)