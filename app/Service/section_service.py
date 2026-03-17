from fastapi import HTTPException
from app.Repository.section_repository import SectionRepository
from app.core.logger import logger


class SectionService:

    def __init__(self, repo: SectionRepository):
        self.repo = repo

    def create_section(self, section_data):
        return self.repo.create_section(section_data)

    def get_section(self, section_id: int):
        section = self.repo.get_section_by_id(section_id)

        if not section:
            logger.warning(f"Section not found id={section_id}")
            raise HTTPException(status_code=404, detail="Section not found")

        return section

    def get_sections(self):
        return self.repo.get_all_sections()

    def update_section(self, section_id: int, update_data):
        section = self.repo.get_section_by_id(section_id)

        if not section:
            logger.warning(f"Update failed, section not found id={section_id}")
            raise HTTPException(status_code=404, detail="Section not found")

        return self.repo.update_section(section, update_data)

    def delete_section(self, section_id: int):
        section = self.repo.get_section_by_id(section_id)

        if not section:
            logger.warning(f"Delete failed, section not found id={section_id}")
            raise HTTPException(status_code=404, detail="Section not found")

        return self.repo.delete_section(section)