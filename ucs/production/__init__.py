from typing import List

from sqlalchemy.orm import Session

from dtos import ProductionDTOResponse, CategoryDTO
from models.production import Production
from repositories import production_repository


def find_production_items(db: Session, category: str | None, year: int | None):
    if category is None and year is None:
        return __to_dto_list(production_repository.find_all(db))

    return __to_dto_list(production_repository.find_by(db, category, year))


def find_production_item(db: Session, prod_id: int):
    return __to_dto(production_repository.find_one(db, prod_id))

def __to_dto(prod: Production) -> ProductionDTOResponse:
    if prod is None:
        return ProductionDTOResponse()

    category = CategoryDTO(name=prod.category.name, meta_name=prod.category.meta_name)
    dto = ProductionDTOResponse(
        id=prod.id,
        name=prod.name,
        quantity=prod.quantity,
        year=prod.year,
        category=category
    )

    return dto

def __to_dto_list(prod: List[Production]) -> List[ProductionDTOResponse]:
    return [__to_dto(prod) for prod in prod]