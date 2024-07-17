import logging
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from dtos import ProductionDTO
from models.production import Production


def create_new(db: Session, dto: ProductionDTO) -> Production:
    dto.id = None

    db_obj = Production(**dto.model_dump())

    try:
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
    except Exception as e:
        logging.error(f'Error while creating production item: {e}')
        raise HTTPException(status_code=500)

    return db_obj


def find_all(db: Session) -> List[Production]:
    return find_by(db, None, None)


def find_one(db: Session, prod_id: int) -> Production:
    return db.query(Production).filter(Production.id == prod_id).first()


def find_by(db: Session, category: str | None, year: int | None) -> List[Production]:
    query = (db.query(Production)
             .order_by(Production.year.desc())
             .order_by(Production.name))

    if category and year:
        query = query.filter(Production.category.has(meta_name=category), Production.year == year)
    elif category:
        query = query.filter(Production.category.has(meta_name=category))
    elif year:
        query = query.filter(Production.year == year)

    return query.all()
