from sqlalchemy.orm import Session

from dtos import CategoryDTO
from dtos import CountryDTO
from repositories import category_repository
from repositories import country_repository


def get_category(db: Session, meta_name: str):
    category_dto = CategoryDTO(meta_name=meta_name, name=meta_name)
    category = category_repository.find_one(db=db, dto=category_dto)
    if not category:
        category = category_repository.create_new(db=db, dto=category_dto)
    return category.id


def get_country(db: Session, name: str) :
    country_dto = CountryDTO(name=name)
    country = country_repository.find_one(db=db, dto=country_dto)
    if not country:
        country = country_repository.create_new(db=db, dto=country_dto)
    return country.id