import logging
from typing import Type

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

def find_all(db: Session) -> list[Type[Production]]:
    return db.query(Production).all()

