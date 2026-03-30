from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from app.core.logger import logger
from app.Repository.user_repository import UserRepository, RoleRepository, UserRoleRepository
from app.schemas.user import UserUpdateRequest, RoleCreateRequest, RoleUpdateRequest


# ══════════════════════════════════════════════════════════════════════════════
# User Service
# ══════════════════════════════════════════════════════════════════════════════

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def get_all_users(self, skip: int = 0, limit: int = 100) -> dict:
        try:
            users = self.repo.get_all(skip, limit)
            total = self.repo.count()

            logger.info(f"Fetched {len(users)} users")

            return {
                "total": total,
                "users": users
            }

        except SQLAlchemyError as e:
            logger.error(f"Database error while fetching users: {str(e)}")

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch users"
            )

    def get_user_by_id(self, user_id: int):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found",
            )
        return user

    def update_user(self, user_id: int, payload: UserUpdateRequest, current_user: dict):
        self._check_self_or_admin(user_id, current_user)

        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found",
            )

        update_data = payload.model_dump(exclude_none=True)
        if "email" in update_data:
            existing = self.repo.get_by_email(update_data["email"])
            if existing and existing.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email is already in use by another account",
                )

        update_data["updated_at"] = datetime.utcnow()
        try:
            return self.repo.update(user, update_data)
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update user",
            )

    def delete_user(self, user_id: int, current_user: dict) -> None:
        self._check_self_or_admin(user_id, current_user)

        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found",
            )
        try:
            self.repo.delete(user)
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete user",
            )

    @staticmethod
    def _check_self_or_admin(target_id: int, current_user: dict) -> None:
        is_admin = "Admin" in current_user.get("roles", [])
        is_self = current_user.get("id") == target_id
        if not (is_admin or is_self):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )


# ══════════════════════════════════════════════════════════════════════════════
# Role Service
# ══════════════════════════════════════════════════════════════════════════════

class RoleService:
    def __init__(self, repo: RoleRepository):
        self.repo = repo

    def get_all_roles(self) -> dict:
        try:
            roles = self.repo.get_all()
            return {"total": len(roles), "roles": roles}
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch roles",
            )

    def get_role_by_id(self, role_id: int):
        role = self.repo.get_by_id(role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Role with id {role_id} not found",
            )
        return role

    def create_role(self, payload: RoleCreateRequest):
        existing = self.repo.get_by_name(payload.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Role '{payload.name}' already exists",
            )
        try:
            return self.repo.create(name=payload.name, description=payload.description)
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create role",
            )

    def update_role(self, role_id: int, payload: RoleUpdateRequest):
        role = self.repo.get_by_id(role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Role with id {role_id} not found",
            )

        update_data = payload.model_dump(exclude_none=True)
        if "name" in update_data:
            conflict = self.repo.get_by_name(update_data["name"])
            if conflict and conflict.id != role_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Role name '{update_data['name']}' is already taken",
                )
        try:
            return self.repo.update(role, update_data)
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update role",
            )

    def delete_role(self, role_id: int) -> None:
        role = self.repo.get_by_id(role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Role with id {role_id} not found",
            )
        try:
            self.repo.delete(role)
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete role",
            )


# ══════════════════════════════════════════════════════════════════════════════
# UserRole Service
# ══════════════════════════════════════════════════════════════════════════════

class UserRoleService:
    def __init__(
        self,
        user_role_repo: UserRoleRepository,
        user_repo: UserRepository,
        role_repo: RoleRepository,
    ):
        self.user_role_repo = user_role_repo
        self.user_repo = user_repo
        self.role_repo = role_repo

    def get_user_roles(self, user_id: int) -> list:
        # Ensure user exists first
        if not self.user_repo.get_by_id(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found",
            )
        try:
            return self.user_role_repo.get_user_roles(user_id)
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch user roles",
            )

    def assign_role(self, user_id: int, role_id: int):
        if not self.user_repo.get_by_id(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found",
            )
        if not self.role_repo.get_by_id(role_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Role with id {role_id} not found",
            )
        # Duplicate check
        existing = self.user_role_repo.get_assignment(user_id, role_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already has this role assigned",
            )
        try:
            return self.user_role_repo.assign(user_id, role_id)
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to assign role",
            )

    def revoke_role(self, user_id: int, role_id: int) -> None:
        assignment = self.user_role_repo.get_assignment(user_id, role_id)
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role assignment not found for this user",
            )
        try:
            self.user_role_repo.revoke(assignment)
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to revoke role",
            )