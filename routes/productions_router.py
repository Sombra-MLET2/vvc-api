import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from dtos import ProductionDTO, ProductionDTOResponse
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


@router.get("/", summary="Production resource list",
            description="Get all production items or a single by using query string `prod_id`",
            response_model=List[ProductionDTOResponse] | ProductionDTOResponse)
async def list_productions(db: Session = Depends(get_db), prod_id: int | None = None):
    print(prod_id)
    if prod_id:
        prod = find_production_item(db, prod_id)

        if not prod:
            return Response(status_code=404)

        return prod

    return find_production_items(db, None, None)


@router.get("/year/{year}", summary="Get production items by `year`", description="Get production items by `year`",
            response_model=List[ProductionDTOResponse])
async def list_productions_by_year(db: Session = Depends(get_db), year: int = None):
    return find_production_items(db, None, year)


@router.get("/category/{category}", summary="Production resource list by category",
            description="Get production items by `category`: tinto, branco, etc.",
            response_model=List[ProductionDTOResponse])
async def list_productions_by_category(db: Session = Depends(get_db), category: str = None):
    return find_production_items(db, category, None)


@router.get("/category/{category}/year/{year}", summary="Production resource list by category and year",
            description="Get production items by `category` and `year`", response_model=List[ProductionDTOResponse])
async def list_productions_by_category_and_year(db: Session = Depends(get_db), category: str = None, year: int = None):
    return find_production_items(db, category, year)


@router.post("/", summary="Production resource add item",
             description="Protected resource that adds production items to the dataset",
             response_model=ProductionDTOResponse)
async def add_production(current_user: Annotated[User, Depends(get_current_active_user)], dto: ProductionDTO,
                         db: Session = Depends(get_db)):
    logger.warning(f'User {current_user.email} is adding a new production item: {dto}')
    return production_repository.create_new(db, dto)
