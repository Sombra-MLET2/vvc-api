import logging
from typing import List

from sqlalchemy.orm import Session

from dtos import CategoryDTO
from models.category import Category


def create_new(db: Session, dto: CategoryDTO) -> Category:
    db_obj = Category(**dto.model_dump())

    try:
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
    except Exception as e:
        logging.error(f'Error while creating production item: {e}')
        raise Exception(f'Error while creating production item {dto.model_dump()}')


    return db_obj


def find_all(db: Session) -> List[Category]:
    return db.query(Category).order_by(Category.name).all()


def find_one(db: Session, dto: CategoryDTO) -> Category:
    return db.query(Category).filter(Category.meta_name == dto.meta_name).first()
