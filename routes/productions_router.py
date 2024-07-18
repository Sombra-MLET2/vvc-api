import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from dtos import ProductionDTO
from infra.database.database import get_db
from infra.security.security import get_current_active_user
from models.user import User
from repositories import production_repository
from ucs.production import find_production_items, find_production_item

router = APIRouter(
    prefix="/productions",
    tags=["productions"],
    responses={401: {"description": "Invalid credentials"},
               404: {"description": "Not found"}},
)

logger = logging.getLogger(__name__)


@router.get("/")
async def list_productions(db: Session = Depends(get_db), prod_id: int | None = None):
    print(prod_id)
    if prod_id:
        prod = find_production_item(db, prod_id)

        if not prod:
            return Response(status_code=404)

        return prod

    return find_production_items(db, None, None)


@router.get("/year/{year}")
async def list_productions_by_year(db: Session = Depends(get_db), year: int = None):
    return find_production_items(db, None, year)


@router.get("/category/{category}")
async def list_productions_by_category(db: Session = Depends(get_db), category: str = None):
    return find_production_items(db, category, None)


@router.get("/category/{category}/year/{year}")
async def list_productions_by_category_year(db: Session = Depends(get_db), category: str = None, year: int = None):
    return find_production_items(db, category, year)


@router.post("/")
async def add_production(current_user: Annotated[User, Depends(get_current_active_user)], dto: ProductionDTO,
                         db: Session = Depends(get_db)):
    """Test Router"""
    logger.warning(f'User {current_user.email} is adding a new production item: {dto}')
    return production_repository.create_new(db, dto)
