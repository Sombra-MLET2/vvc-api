from typing import List

from sqlalchemy.orm import Session

from dtos import CategoryDTO, ImportDTOResponse, ImportDTO
from infra.cache.caching_keys import vvc_cache
from models.imports import Import
from repositories import imports_repository


@vvc_cache()
async def find_imports_items(db: Session, category: str | None, year: int | None, country: str | None):
    if category is None and year is None and country is None:
        return __to_dto_list(imports_repository.find_all(db))

    return __to_dto_list(imports_repository.find_by(db, category, year, country))


@vvc_cache()
async def find_imports_item(db: Session, imp_id: int):
    return __to_dto(imports_repository.find_one(db, imp_id))


def add_import_item(db: Session, dto: ImportDTO) -> ImportDTOResponse:
    return __to_dto(imports_repository.create_new(db, dto))

def __to_dto(imp: Import) -> ImportDTOResponse | None:
    if imp is None:
        return None

    category = CategoryDTO(name=imp.category.name, meta_name=imp.category.meta_name)

    dto = ImportDTOResponse(
        id=imp.id,
        quantity=imp.quantity,
        year=imp.year,
        category=category,
        country=imp.country.name
    )

    return dto

def __to_dto_list(imports: List[Import]) -> List[ImportDTOResponse]:
    return [__to_dto(imp) for imp in imports]