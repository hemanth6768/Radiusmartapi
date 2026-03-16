from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.section import SectionCreate, SectionUpdate, SectionResponse
from app.Service.section_service import SectionService


router = APIRouter(
    prefix="/sections",
    tags=["Sections"]
)


@router.post("/", response_model=SectionResponse)
def create_section(section: SectionCreate, db: Session = Depends(get_db)):
    return SectionService.create_section(db, section)


@router.get("/", response_model=List[SectionResponse])
def get_sections(db: Session = Depends(get_db)):
    return SectionService.get_sections(db)


@router.get("/{section_id}", response_model=SectionResponse)
def get_section(section_id: int, db: Session = Depends(get_db)):
    return SectionService.get_section(db, section_id)


@router.put("/{section_id}", response_model=SectionResponse)
def update_section(section_id: int, section: SectionUpdate, db: Session = Depends(get_db)):
    return SectionService.update_section(db, section_id, section)


@router.delete("/{section_id}")
def delete_section(section_id: int, db: Session = Depends(get_db)):
    return SectionService.delete_section(db, section_id)