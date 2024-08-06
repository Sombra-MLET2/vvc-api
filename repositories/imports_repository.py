import logging
from typing import List

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from dtos import ImportDTO
from models.country import Country
from models.imports import Import


def create_new(db: Session, dto: ImportDTO) -> Import:
    dto.id = None

    db_obj = Import(**dto.model_dump())

    try:
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
    except Exception as e:
        logging.error(f'Error while creating imports item: {e}')
        raise HTTPException(status_code=500)

    return db_obj


def create_new(db: Session, data: list):
    db_obj = [Import(**_dto.model_dump()) for _dto in data]

    try:
        db.add_all(db_obj)
        db.commit()
    except Exception as e:
        db.rollback()
        logging.error(f'Error while creating import item: {e}')
        raise Exception(e)


def find_all(db: Session) -> List[Import]:
    return find_by(db, None, None, None)


def find_one(db: Session, imp_id: int) -> Import:
    return db.query(Import).filter(Import.id == imp_id).first()


def find_one(db: Session, dto: ImportDTO) -> Import:
    return db.query(Import).filter(Import.quantity == dto.quantity,
                                   Import.value == dto.value,
                                   Import.year == dto.year,
                                   Import.category_id == dto.category_id,
                                   Import.country_id == dto.country_id).first()


def find_by(db: Session, category: str | None, year: int | None, country: str | None) -> List[Import]:
    query = (db.query(Import)
             .join(Country, Import.country_id == Country.id)
             .order_by(Import.year.desc())
             .order_by(Country.name))

    if category and year:
        query = query.filter(Import.category.has(meta_name=category), Import.year == year)
    elif category:
        query = query.filter(Import.category.has(meta_name=category))
    elif year:
        query = query.filter(Import.year == year)

    if country:
        query = query.filter(Import.country.has(func.lower(country) == func.lower(Country.name)))

    return query.all()
