from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.models.userrole import UserRole
from app.models.rolepermission import RolePermission

from app.Repository.auth_repository import AuthRepository
from app.core.security import hash_password ,verify_password ,create_access_token
from app.core.logger import logger


class AuthService:

    @staticmethod
    def signup(db: Session, data):

        logger.info("Signup attempt for %s", data.email)

        existing = AuthRepository.get_user_by_email(db, data.email)

        if existing:
            logger.warning("Email already exists %s", data.email)

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

        return AuthRepository.create_user(db, user)
    

    @staticmethod
    def login(db: Session, data):

        logger.info("Login attempt for %s", data.email)

        user = AuthRepository.get_user_by_email(db, data.email)

        if not user:
            logger.warning("User not found %s", data.email)

            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        if not verify_password(data.password, user.password_hash):

            logger.warning("Invalid password for %s", data.email)

            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        token = create_access_token({"sub": str(user.id)})

        return token
    
    @staticmethod
    def create_role(db: Session, data):

        role = Role(
            name=data.name,
            description=data.description
        )

        return AuthRepository.create_role(db, role)
    

    @staticmethod
    def create_permission(db: Session, data):

        permission = Permission(
            name=data.name,
            description=data.description
        )

        return AuthRepository.create_permission(db, permission)
    

    @staticmethod
    def assign_role(db: Session, data):

        user_role = UserRole(
            user_id=data.user_id,
            role_id=data.role_id
        )

        return AuthRepository.assign_role(db, user_role)

    @staticmethod
    def assign_permission(db: Session, data):

        role_permission = RolePermission(
            role_id=data.role_id,
            permission_id=data.permission_id
        )

        return AuthRepository.assign_permission(db, role_permission)