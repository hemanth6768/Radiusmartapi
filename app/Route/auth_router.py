from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.auth import AssignRoleRequest,AssignPermissionRequest, PermissionCreate,TokenResponse ,SignupRequest,LoginRequest,RoleCreate
from app.Service.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
def signup(request: SignupRequest, db: Session = Depends(get_db)):

    user = AuthService.signup(db, request)

    return {
        "message": "User created",
        "user_id": user.id
    }

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):

    token = AuthService.login(db, request)

    return {
        "access_token": token
    }

@router.post("/roles")
def create_role(request: RoleCreate, db: Session = Depends(get_db)):

    role = AuthService.create_role(db, request)

    return role

@router.post("/permissions")
def create_permission(request: PermissionCreate, db: Session = Depends(get_db)):

    permission = AuthService.create_permission(db, request)

    return permission


@router.post("/assign-role")
def assign_role(request: AssignRoleRequest, db: Session = Depends(get_db)):

    return AuthService.assign_role(db, request)


@router.post("/assign-permission")
def assign_permission(request: AssignPermissionRequest, db: Session = Depends(get_db)):

    return AuthService.assign_permission(db, request)