import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from dtos import ProcessingDTO
from infra.database.database import get_db
from infra.security.security import get_current_active_user
from models.user import User
from repositories import processing_repository
from ucs.processing import find_processing_item, find_processing_items

router = APIRouter(
    prefix="/processing",
    tags=["processing"],
    responses={401: {"description": "Invalid credentials"},
               404: {"description": "Not found"}},
)

logger = logging.getLogger(__name__)


@router.get("/")
async def list_processing(db: Session = Depends(get_db), prod_id: int | None = None):
    print(prod_id)
    if prod_id:
        prod = find_processing_item(db, prod_id)

        if not prod:
            return Response(status_code=404)

        return prod

    return find_processing_items(db, None, None, None)


@router.get("/year/{year}")
async def list_processing_by_year(db: Session = Depends(get_db), year: int = None):
    return find_processing_items(db, None, year, None)


@router.get("/category/{category}")
async def list_processing_by_category(db: Session = Depends(get_db), category: str = None):
    return find_processing_items(db, category, None, None)

@router.get("/grape/{grape}")
async def list_processing_by_category(db: Session = Depends(get_db), grape: str = None):
    return find_processing_items(db, None, None, grape)

@router.get("/grape/{grape}/year/{year}")
async def list_processing_by_category(db: Session = Depends(get_db), grape: str = None, year: int = None):
    return find_processing_items(db, None, year, grape)


@router.get("/category/{category}/year/{year}")
async def list_processing_by_category_year(db: Session = Depends(get_db), category: str = None, year: int = None):
    return find_processing_items(db, category, year, None)


@router.post("/")
async def add_processing(current_user: Annotated[User, Depends(get_current_active_user)], dto: ProcessingDTO,
                         db: Session = Depends(get_db)):
    logger.warning(f'User {current_user.email} is adding a new processing item: {dto}')
    return processing_repository.create_new(db, dto)
