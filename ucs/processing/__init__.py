from typing import List

from sqlalchemy.orm import Session

from dtos import CategoryDTO, ProcessingDTOResponse
from models.processing import Processing
from repositories import processing_repository


def find_processing_items(db: Session, category: str | None, year: int | None, grape: str | None):
    if category is None and year is None and grape is None:
        return __to_dto_list(processing_repository.find_all(db))

    return __to_dto_list(processing_repository.find_by(db, category, year, grape))


def find_processing_item(db: Session, proc_id: int):
    return __to_dto(processing_repository.find_one(db, proc_id))

def __to_dto(proc: Processing) -> ProcessingDTOResponse:
    if proc is None:
        return ProcessingDTOResponse()

    category = CategoryDTO(name=proc.category.name, meta_name=proc.category.meta_name)
    grape_class = CategoryDTO(name=proc.grape_class.name, meta_name=proc.grape_class.meta_name)
    dto = ProcessingDTOResponse(
        id=proc.id,
        cultivation=proc.cultivation,
        quantity=proc.quantity,
        year=proc.year,
        category=category,
        grape_class=grape_class,
    )

    return dto

def __to_dto_list(proc: List[Processing]) -> List[ProcessingDTOResponse]:
    return [__to_dto(proc) for proc in proc]