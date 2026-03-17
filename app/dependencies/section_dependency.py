from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.Repository.section_repository import SectionRepository
from app.Service.section_service import SectionService


def get_section_repository(
    db: Session = Depends(get_db)
) -> SectionRepository:
    return SectionRepository(db)


def get_section_service(
    repo: SectionRepository = Depends(get_section_repository)
) -> SectionService:
    return SectionService(repo)