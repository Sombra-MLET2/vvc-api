from typing import List

from sqlalchemy.orm import Session

from dtos import CategoryDTO
from models.category import Category


def create_new(db: Session, dto: CategoryDTO) -> Category:
    pass


def find_all(db: Session) -> List[Category]:
    return db.query(Category).order_by(Category.name).all()
