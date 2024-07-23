from typing import List

from sqlalchemy.orm import Session

from dtos import SaleDTOResponse, CategoryDTO
from models.sale import Sale
from repositories import sale_repository


def find_sales_items(db: Session, category: str | None, year: int | None):
    if category is None and year is None:
        return __to_dto_list(sale_repository.find_all(db))

    return __to_dto_list(sale_repository.find_by(db, category, year))


def find_sales_item(db: Session, sale_id: int):
    return __to_dto(sale_repository.find_one(db, sale_id))

def __to_dto(sale: Sale) -> SaleDTOResponse:
    if sale is None:
        return SaleDTOResponse()

    category = CategoryDTO(name=sale.category.name, meta_name=sale.category.meta_name)
    dto = SaleDTOResponse(
        id=sale.id,
        name=sale.name,
        quantity=sale.quantity,
        year=sale.year,
        category=category
    )

    return dto

def __to_dto_list(sales: List[Sale]) -> List[SaleDTOResponse]:
    return [__to_dto(sale) for sale in sales]