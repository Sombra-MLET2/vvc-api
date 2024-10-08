from typing import List

from sqlalchemy.orm import Session

from dtos import ProcessingDTOResponse, ProcessingDTO
from infra.cache.caching_keys import vvc_cache
from models.processing import Processing
from repositories import processing_repository
from ucs.categories import to_dto as to_category_dto


@vvc_cache()
async def find_processing_items(db: Session, category: str | None, year: int | None, grape: str | None):
    if category is None and year is None and grape is None:
        return __to_dto_list(processing_repository.find_all(db))

    return __to_dto_list(processing_repository.find_by(db, category, year, grape))


@vvc_cache()
async def find_processing_item(db: Session, proc_id: int):
    return __to_dto(processing_repository.find_one(db, proc_id))


def add_new_processing_item(db: Session, dto: ProcessingDTO) -> ProcessingDTOResponse:
    return __to_dto(processing_repository.create_new(db, dto))


def __to_dto(proc: Processing) -> ProcessingDTOResponse | None:
    if proc is None:
        return None

    category = to_category_dto(proc.category)
    grape_class = to_category_dto(proc.grape_class)
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
