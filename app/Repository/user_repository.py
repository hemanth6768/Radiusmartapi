from typing import Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from app.core.logger import logger
from app.models.user import User
from app.models.role import Role
from app.models.userrole import UserRole


# ══════════════════════════════════════════════════════════════════════════════
# User Repository
# ══════════════════════════════════════════════════════════════════════════════

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    
    def get_all(self, skip: int = 0, limit: int = 100) -> list[User]:
      return (
        self.db.query(User)
        .options(
            joinedload(User.id).joinedload(UserRole.user_id)   # ✅ FIX
        )
        .order_by(User.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def count(self) -> int:
        return self.db.query(User).count()

    def update(self, user: User, data: dict) -> User:
        try:
            for key, value in data.items():
                setattr(user, key, value)
            self.db.commit()
            self.db.refresh(user)
            return user
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def delete(self, user: User) -> None:
        try:
            self.db.delete(user)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e


# ══════════════════════════════════════════════════════════════════════════════
# Role Repository
# ══════════════════════════════════════════════════════════════════════════════

class RoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Role]:
        return self.db.query(Role).all()

    def get_by_id(self, role_id: int) -> Optional[Role]:
        return self.db.query(Role).filter(Role.id == role_id).first()

    def get_by_name(self, name: str) -> Optional[Role]:
        return self.db.query(Role).filter(Role.name == name).first()

    def count(self) -> int:
        return self.db.query(Role).count()

    def create(self, name: str, description: Optional[str]) -> Role:
        try:
            role = Role(name=name, description=description)
            self.db.add(role)
            self.db.commit()
            self.db.refresh(role)
            return role
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def update(self, role: Role, data: dict) -> Role:
        try:
            for key, value in data.items():
                setattr(role, key, value)
            self.db.commit()
            self.db.refresh(role)
            return role
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def delete(self, role: Role) -> None:
        try:
            self.db.delete(role)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e


# ══════════════════════════════════════════════════════════════════════════════
# UserRole Repository
# ══════════════════════════════════════════════════════════════════════════════

class UserRoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_roles(self, user_id: int) -> list[UserRole]:
        return (
            self.db.query(UserRole)
            .filter(UserRole.user_id == user_id)
            .all()
        )

    def get_assignment(self, user_id: int, role_id: int) -> Optional[UserRole]:
        return (
            self.db.query(UserRole)
            .filter(UserRole.user_id == user_id, UserRole.role_id == role_id)
            .first()
        )

    def assign(self, user_id: int, role_id: int) -> UserRole:
        try:
            user_role = UserRole(user_id=user_id, role_id=role_id)
            self.db.add(user_role)
            self.db.commit()
            self.db.refresh(user_role)
            return user_role
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def revoke(self, user_role: UserRole) -> None:
        try:
            self.db.delete(user_role)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def revoke_all(self, user_id: int) -> None:
        """Remove all roles from a user — used before user deletion."""
        try:
            self.db.query(UserRole).filter(UserRole.user_id == user_id).delete()
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e