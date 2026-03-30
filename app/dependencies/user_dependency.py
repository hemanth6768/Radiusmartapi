from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.Repository.user_repository import UserRepository, RoleRepository, UserRoleRepository
from app.Service.user_service import UserService, RoleService, UserRoleService


# ── Repositories ──────────────────────────────────────────────────────────────

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_role_repository(db: Session = Depends(get_db)) -> RoleRepository:
    return RoleRepository(db)


def get_user_role_repository(db: Session = Depends(get_db)) -> UserRoleRepository:
    return UserRoleRepository(db)


# ── Services ──────────────────────────────────────────────────────────────────

def get_user_service(
    repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(repo)


def get_role_service(
    repo: RoleRepository = Depends(get_role_repository),
) -> RoleService:
    return RoleService(repo)


def get_user_role_service(
    user_role_repo: UserRoleRepository = Depends(get_user_role_repository),
    user_repo: UserRepository = Depends(get_user_repository),
    role_repo: RoleRepository = Depends(get_role_repository),
) -> UserRoleService:
    return UserRoleService(user_role_repo, user_repo, role_repo)