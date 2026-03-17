# app/service/auth_service.py

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.models.userrole import UserRole
from app.models.rolepermission import RolePermission

from app.Repository.auth_repository import AuthRepository
from app.core.security import hash_password, verify_password, create_access_token
from app.core.logger import logger


class AuthService:

    def __init__(self, repo: AuthRepository):
        self.repo = repo

    def signup(self, data):

        logger.info("Signup attempt: %s", data.email)

        try:
            existing = self.repo.get_user_by_email(data.email)

            if existing:
                raise HTTPException(
                    status_code=400,
                    detail="Email already registered"
                )

            user = User(
                email=data.email,
                password_hash=hash_password(data.password),
                first_name=data.first_name,
                last_name=data.last_name
            )

            self.repo.create_user(user)
            self.repo.db.commit()

            logger.info("User created: %s", data.email)

            return user

        except IntegrityError:
            self.repo.db.rollback()
            raise HTTPException(400, "User already exists")

        except SQLAlchemyError as e:
            self.repo.db.rollback()
            logger.error(f"DB error: {str(e)}")
            raise HTTPException(500, "Internal server error")


    def login(self, data):

        logger.info("Login attempt: %s", data.email)

        user = self.repo.get_user_by_email(data.email)

        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        return create_access_token({"sub": str(user.id)})


    def create_role(self, data):
        try:
            role = Role(name=data.name, description=data.description)
            self.repo.create_role(role)
            self.repo.db.commit()
            return role

        except IntegrityError:
            self.repo.db.rollback()
            raise HTTPException(400, "Role already exists")

        except SQLAlchemyError:
            self.repo.db.rollback()
            raise HTTPException(500, "Failed to create role")


    def create_permission(self, data):
        try:
            permission = Permission(name=data.name, description=data.description)
            self.repo.create_permission(permission)
            self.repo.db.commit()
            return permission

        except IntegrityError:
            self.repo.db.rollback()
            raise HTTPException(400, "Permission already exists")

        except SQLAlchemyError:
            self.repo.db.rollback()
            raise HTTPException(500, "Failed to create permission")


    def assign_role(self, data):
        try:
            user_role = UserRole(user_id=data.user_id, role_id=data.role_id)
            self.repo.assign_role(user_role)
            self.repo.db.commit()
            return user_role

        except IntegrityError:
            self.repo.db.rollback()
            raise HTTPException(400, "Role already assigned")

        except SQLAlchemyError:
            self.repo.db.rollback()
            raise HTTPException(500, "Failed to assign role")


    def assign_permission(self, data):
        try:
            role_permission = RolePermission(
                role_id=data.role_id,
                permission_id=data.permission_id
            )
            self.repo.assign_permission(role_permission)
            self.repo.db.commit()
            return role_permission

        except IntegrityError:
            self.repo.db.rollback()
            raise HTTPException(400, "Permission already assigned")

        except SQLAlchemyError:
            self.repo.db.rollback()
            raise HTTPException(500, "Failed to assign permission")