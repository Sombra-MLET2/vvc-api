import logging
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from dtos import SaleDTO
from models.sale import Sale


def create_new(db: Session, dto: SaleDTO) -> Sale:
    dto.id = None

    db_obj = Sale(**dto.model_dump())

    try:
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
    except Exception as e:
        logging.error(f'Error while creating Sale item: {e}')
        raise HTTPException(status_code=500)

    return db_obj


def create_new(db: Session, data: list):
    db_obj = [Sale(**_dto.model_dump()) for _dto in data]

    try:
        db.add_all(db_obj)
        db.commit()
    except Exception as e:
        db.rollback()
        logging.error(f'Error while creating production item: {e}')
        raise Exception(e)


def find_all(db: Session) -> List[Sale]:
    return find_by(db, None, None)


def find_one(db: Session, sale_id: int) -> Sale:
    return db.query(Sale).filter(Sale.id == sale_id).first()


def find_one(db: Session, dto: SaleDTO) -> Sale:
    return db.query(Sale).filter(Sale.name == dto.name,
                                 Sale.quantity == dto.quantity,
                                 Sale.year == dto.year,
                                 Sale.category_id == dto.category_id).first()


def find_by(db: Session, category: str | None, year: int | None) -> List[Sale]:
    query = (db.query(Sale)
             .order_by(Sale.year.desc())
             .order_by(Sale.name))

    if category and year:
        query = query.filter(Sale.category.has(meta_name=category), Sale.year == year)
    elif category:
        query = query.filter(Sale.category.has(meta_name=category))
    elif year:
        query = query.filter(Sale.year == year)

    return query.all()
