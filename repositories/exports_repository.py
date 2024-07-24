import logging
from typing import List

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from dtos import ExportDTO
from models.country import Country
from models.exportation import Exportation


def create_new(db: Session, dto: ExportDTO) -> Exportation:
    dto.id = None

    db_obj = Exportation(**dto.model_dump())

    try:
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
    except Exception as e:
        logging.error(f'Error while creating exports item: {e}')
        raise HTTPException(status_code=500)

    return db_obj


def find_all(db: Session) -> List[Exportation]:
    return find_by(db, None, None, None)


def find_one(db: Session, exp_id: int) -> Exportation:
    return db.query(Exportation).filter(Exportation.id == exp_id).first()


def find_by(db: Session, category: str | None, year: int | None, country: str | None) -> List[Exportation]:
    query = (db.query(Exportation)
             .join(Country, Exportation.country_id == Country.id)
             .order_by(Exportation.year.desc())
             .order_by(Country.name))

    if category and year:
        query = query.filter(Exportation.category.has(meta_name=category), Exportation.year == year)
    elif category:
        query = query.filter(Exportation.category.has(meta_name=category))
    elif year:
        query = query.filter(Exportation.year == year)

    if country:
        query = query.filter(Exportation.country.has(func.lower(country) == func.lower(Country.name)))

    return query.all()
