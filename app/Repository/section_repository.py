from sqlalchemy.orm import Session
from app.models.section import Section
from app.core.logger import logger


class SectionRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_section(self, section_data):
        try:
            section = Section(**section_data.dict())
            self.db.add(section)
            self.db.commit()
            self.db.refresh(section)

            logger.info(f"Section created id={section.id}")
            return section

        except Exception as e:
            logger.error(f"Create failed: {str(e)}")
            self.db.rollback()
            raise

    def get_section_by_id(self, section_id: int):
        return self.db.query(Section).filter(Section.id == section_id).first()

    def get_all_sections(self):
        return (
            self.db.query(Section)
            .filter(Section.is_active == True)
            .order_by(Section.display_order)
            .all()
        )

    def update_section(self, section, update_data):
        try:
            for key, value in update_data.dict(exclude_unset=True).items():
                setattr(section, key, value)

            self.db.commit()
            self.db.refresh(section)

            logger.info(f"Section updated id={section.id}")
            return section

        except Exception as e:
            logger.error(f"Update failed: {str(e)}")
            self.db.rollback()
            raise

    def delete_section(self, section):
        try:
            section.is_active = False
            self.db.commit()

            logger.info(f"Section deleted id={section.id}")
            return section

        except Exception as e:
            logger.error(f"Delete failed: {str(e)}")
            self.db.rollback()
            raise