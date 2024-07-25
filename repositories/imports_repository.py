import logging
from typing import List

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from dtos import ImportDTO
from models.country import Country
from models.importation import Importation


def create_new(db: Session, dto: ImportDTO) -> Importation:
    dto.id = None

    db_obj = Importation(**dto.model_dump())

    try:
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
    except Exception as e:
        logging.error(f'Error while creating imports item: {e}')
        raise HTTPException(status_code=500)

    return db_obj


def find_all(db: Session) -> List[Importation]:
    return find_by(db, None, None, None)


def find_one(db: Session, imp_id: int) -> Importation:
    return db.query(Importation).filter(Importation.id == imp_id).first()


def find_by(db: Session, category: str | None, year: int | None, country: str | None) -> List[Importation]:
    query = (db.query(Importation)
             .join(Country, Importation.country_id == Country.id)
             .order_by(Importation.year.desc())
             .order_by(Country.name))

    if category and year:
        query = query.filter(Importation.category.has(meta_name=category), Importation.year == year)
    elif category:
        query = query.filter(Importation.category.has(meta_name=category))
    elif year:
        query = query.filter(Importation.year == year)

    if country:
        query = query.filter(Importation.country.has(func.lower(country) == func.lower(Country.name)))

    return query.all()
