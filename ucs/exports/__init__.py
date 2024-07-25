from typing import List

from sqlalchemy.orm import Session

from dtos import CategoryDTO, ExportDTOResponse, ExportDTO
from models.exports import Export
from repositories import exports_repository


def find_exports_items(db: Session, category: str | None, year: int | None, country: str | None):
    if category is None and year is None and country is None:
        return __to_dto_list(exports_repository.find_all(db))

    return __to_dto_list(exports_repository.find_by(db, category, year, country))


def find_exports_item(db: Session, exp_id: int):
    return __to_dto(exports_repository.find_one(db, exp_id))


def add_export_item(db: Session, dto: ExportDTO) -> ExportDTOResponse:
    return __to_dto(exports_repository.create_new(db, dto))

def __to_dto(exp: Export) -> ExportDTOResponse:
    if exp is None:
        return ExportDTOResponse()

    category = CategoryDTO(name=exp.category.name, meta_name=exp.category.meta_name)

    dto = ExportDTOResponse(
        id=exp.id,
        quantity=exp.quantity,
        year=exp.year,
        category=category,
        country=exp.country.name
    )

    return dto

def __to_dto_list(exports: List[Export]) -> List[ExportDTOResponse]:
    return [__to_dto(exp) for exp in exports]