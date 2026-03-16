from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.Repository.section_repository import SectionRepository


class SectionService:

    @staticmethod
    def create_section(db: Session, section_data):
        return SectionRepository.create_section(db, section_data)

    @staticmethod
    def get_section(db: Session, section_id: int):

        section = SectionRepository.get_section_by_id(db, section_id)

        if not section:
            raise HTTPException(status_code=404, detail="Section not found")

        return section

    @staticmethod
    def get_sections(db: Session):
        return SectionRepository.get_all_sections(db)

    @staticmethod
    def update_section(db: Session, section_id: int, update_data):

        section = SectionRepository.get_section_by_id(db, section_id)

        if not section:
            raise HTTPException(status_code=404, detail="Section not found")

        return SectionRepository.update_section(db, section, update_data)

    @staticmethod
    def delete_section(db: Session, section_id: int):

        section = SectionRepository.get_section_by_id(db, section_id)

        if not section:
            raise HTTPException(status_code=404, detail="Section not found")

        return SectionRepository.delete_section(db, section)