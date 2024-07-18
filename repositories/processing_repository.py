import logging
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from dtos import ProcessingDTO
from models.processing import Processing


def create_new(db: Session, dto: ProcessingDTO) -> Processing:
    dto.id = None

    db_obj = Processing(**dto.model_dump())

    try:
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
    except Exception as e:
        logging.error(f'Error while creating processing item: {e}')
        raise HTTPException(status_code=500)

    return db_obj


def find_all(db: Session) -> List[Processing]:
    return find_by(db, None, None)


def find_one(db: Session, pro_id: int) -> Processing:
    return db.query(Processing).filter(Processing.id == pro_id).first()


def find_by(db: Session, category: str | None, year: int | None, grape: str | None) -> List[Processing]:
    query = (db.query(Processing)
             .order_by(Processing.year.desc())
             .order_by(Processing.cultivation))

    if category and year:
        query = query.filter(Processing.category.has(meta_name=category), Processing.year == year)
    elif category:
        query = query.filter(Processing.category.has(meta_name=category))
    elif year:
        query = query.filter(Processing.year == year)

    if grape:
        query = query.filter(Processing.grape_class.has(meta_name=grape))

    return query.all()
