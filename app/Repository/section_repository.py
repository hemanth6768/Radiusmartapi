from sqlalchemy.orm import Session
from app.models.section import Section


class SectionRepository:

    @staticmethod
    def create_section(db: Session, section_data):
        section = Section(**section_data.dict())
        db.add(section)
        db.commit()
        db.refresh(section)
        return section

    @staticmethod
    def get_section_by_id(db: Session, section_id: int):
        return db.query(Section).filter(Section.id == section_id).first()

    @staticmethod
    def get_all_sections(db: Session):
        return db.query(Section).filter(Section.is_active == True).order_by(Section.display_order).all()

    @staticmethod
    def update_section(db: Session, section, update_data):
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(section, key, value)

        db.commit()
        db.refresh(section)
        return section

    @staticmethod
    def delete_section(db: Session, section):
        section.is_active = False
        db.commit()
        return section