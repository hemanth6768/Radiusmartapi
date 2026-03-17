# app/repository/auth_repository.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.models.userrole import UserRole
from app.models.rolepermission import RolePermission

from app.core.logger import logger


class AuthRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str):
        try:
            logger.info(f"[Repo] Fetching user by email: {email}")

            user = self.db.query(User).filter(User.email == email).first()

            if user:
                logger.info(f"[Repo] User found: {email}")
            else:
                logger.info(f"[Repo] User not found: {email}")

            return user

        except SQLAlchemyError as e:
            logger.error(f"[Repo] DB error in get_user_by_email: {str(e)}")
            raise


    def create_user(self, user: User):
        try:
            logger.info(f"[Repo] Creating user: {user.email}")

            self.db.add(user)
            self.db.flush()

            logger.info(f"[Repo] User staged for commit: {user.email}")

            return user

        except SQLAlchemyError as e:
            logger.error(f"[Repo] Error creating user: {str(e)}")
            raise


    def create_role(self, role: Role):
        try:
            logger.info(f"[Repo] Creating role: {role.name}")

            self.db.add(role)
            self.db.flush()

            return role

        except SQLAlchemyError as e:
            logger.error(f"[Repo] Error creating role: {str(e)}")
            raise


    def create_permission(self, permission: Permission):
        try:
            logger.info(f"[Repo] Creating permission: {permission.name}")

            self.db.add(permission)
            self.db.flush()

            return permission

        except SQLAlchemyError as e:
            logger.error(f"[Repo] Error creating permission: {str(e)}")
            raise


    def assign_role(self, user_role: UserRole):
        try:
            logger.info(
                f"[Repo] Assigning role {user_role.role_id} to user {user_role.user_id}"
            )

            self.db.add(user_role)
            self.db.flush()

            return user_role

        except SQLAlchemyError as e:
            logger.error(f"[Repo] Error assigning role: {str(e)}")
            raise


    def assign_permission(self, role_permission: RolePermission):
        try:
            logger.info(
                f"[Repo] Assigning permission {role_permission.permission_id} "
                f"to role {role_permission.role_id}"
            )

            self.db.add(role_permission)
            self.db.flush()

            return role_permission

        except SQLAlchemyError as e:
            logger.error(f"[Repo] Error assigning permission: {str(e)}")
            raise