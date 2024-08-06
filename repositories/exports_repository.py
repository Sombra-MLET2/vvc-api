import logging
from typing import List

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from dtos import ExportDTO
from models.country import Country
from models.exports import Export


def create_new(db: Session, dto: ExportDTO) -> Export:
    dto.id = None

    db_obj = Export(**dto.model_dump())

    try:
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
    except Exception as e:
        logging.error(f'Error while creating exports item: {e}')
        raise HTTPException(status_code=500)

    return db_obj


def create_new(db: Session, data: list):
    db_obj = [Export(**_dto.model_dump()) for _dto in data]

    try:
        db.add_all(db_obj)
        db.commit()
    except Exception as e:
        db.rollback()
        logging.error(f'Error while creating export item: {e}')
        raise Exception(e)


def find_all(db: Session) -> List[Export]:
    return find_by(db, None, None, None)


def find_one(db: Session, exp_id: int) -> Export:
    return db.query(Export).filter(Export.id == exp_id).first()


def find_one(db: Session, dto: ExportDTO) -> Export:
    return db.query(Export).filter(Export.quantity == dto.quantity,
                                   Export.value == dto.value,
                                   Export.year == dto.year,
                                   Export.category_id == dto.category_id,
                                   Export.country_id == dto.country_id).first()


def find_by(db: Session, category: str | None, year: int | None, country: str | None) -> List[Export]:
    query = (db.query(Export)
             .join(Country, Export.country_id == Country.id)
             .order_by(Export.year.desc())
             .order_by(Country.name))

    if category and year:
        query = query.filter(Export.category.has(meta_name=category), Export.year == year)
    elif category:
        query = query.filter(Export.category.has(meta_name=category))
    elif year:
        query = query.filter(Export.year == year)

    if country:
        query = query.filter(Export.country.has(func.lower(country) == func.lower(Country.name)))

    return query.all()
