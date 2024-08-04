from sqlalchemy.orm import Session

from dtos import CategoryDTO
from dtos import CountryDTO
from models.category import Category
from models.country import Country
from repositories import category_repository
from repositories import country_repository


def get_category(db: Session, meta_name: str):
    category_dto = CategoryDTO(meta_name=meta_name, name=meta_name)
    category = category_repository.find_one(db=db, dto=category_dto)
    if not category:
        category = category_repository.create_new(db=db, dto=category_dto)
    return category.id


def get_country(db: Session, meta_name: str) :
    pass