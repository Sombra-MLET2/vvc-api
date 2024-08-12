from sqlalchemy.orm import Session

from dtos import CategoryDTO
from dtos import CountryDTO
from models.category import Category
from repositories import category_repository
from repositories import country_repository


def create_category(db: Session, category_dto: CategoryDTO) -> Category:
    return category_repository.create_new(db=db, dto=category_dto)


def get_category(db: Session, name: str, meta_name: str = ""):
    category_dto = CategoryDTO(name=name, meta_name=meta_name)

    category = category_repository.find_one(db=db, dto=category_dto)

    if not category:
        category = create_category(db=db, category_dto=category_dto)

    return category.id
