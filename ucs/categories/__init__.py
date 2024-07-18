from typing import List

from sqlalchemy.orm import Session

from dtos import CategoryDTO, CategoryWithIdDTO
from models.category import Category
from repositories.category_repository import find_all


def to_dto(cat: Category) -> CategoryDTO:
    return CategoryDTO(name=cat.name, meta_name=cat.meta_name)


def __to_id_dto(cat: Category) -> CategoryWithIdDTO:
    return CategoryWithIdDTO(id=cat.id, name=cat.name, meta_name=cat.meta_name)


def __to_dto_list(categories: List[Category]):
    return [__to_id_dto(cat) for cat in categories]


def list_all_categories(db: Session) -> List[CategoryDTO]:
    return __to_dto_list(find_all(db))
