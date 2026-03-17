
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db

from app.Repository.auth_repository import AuthRepository
from app.Service.auth_service import AuthService


def get_auth_repository(db: Session = Depends(get_db)):
    return AuthRepository(db)


def get_auth_service(
    repo: AuthRepository = Depends(get_auth_repository)
):
    return AuthService(repo)