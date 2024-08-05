import logging
from typing import List

from sqlalchemy.orm import Session

from dtos import CountryDTO
from models.country import Country


def create_new(db: Session, dto: CountryDTO) -> Country:
    db_obj = Country(**dto.model_dump())

    try:
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
    except Exception as e:
        logging.error(f'Error while creating production item: {e}')
        raise Exception(f'Error while creating production item {dto.model_dump()}')


    return db_obj


def find_all(db: Session) -> List[Country]:
    return db.query(Country).order_by(Country.name).all()


def find_one(db: Session, dto: CountryDTO) -> Country:
    return db.query(Country).filter(Country.name == dto.name).first()
