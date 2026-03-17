from fastapi import APIRouter, Depends
from typing import List

from app.schemas.section import SectionCreate, SectionUpdate, SectionResponse
from app.Service.section_service import SectionService
from app.dependencies.section_dependency import get_section_service


router = APIRouter(
    prefix="/sections",
    tags=["Sections"]
)


@router.post("/", response_model=SectionResponse)
def create_section(
    section: SectionCreate,
    service: SectionService = Depends(get_section_service)
):
    return service.create_section(section)


@router.get("/", response_model=List[SectionResponse])
def get_sections(
    service: SectionService = Depends(get_section_service)
):
    return service.get_sections()


@router.get("/{section_id}", response_model=SectionResponse)
def get_section(
    section_id: int,
    service: SectionService = Depends(get_section_service)
):
    return service.get_section(section_id)


@router.put("/{section_id}", response_model=SectionResponse)
def update_section(
    section_id: int,
    section: SectionUpdate,
    service: SectionService = Depends(get_section_service)
):
    return service.update_section(section_id, section)


@router.delete("/{section_id}")
def delete_section(
    section_id: int,
    service: SectionService = Depends(get_section_service)
):
    return service.delete_section(section_id)