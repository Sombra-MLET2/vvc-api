import logging
from typing import Annotated, List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import Response

from dtos import SaleDTO, SaleDTOResponse
from infra.converter.fast_api_csv_converter import handle_csv_response
from infra.database.database import get_db
from infra.security.security import get_current_active_user
from models.user import User
from repositories import sale_repository
from ucs.sale import find_sales_items, find_sales_item

router = APIRouter(
    prefix="/sales",
    tags=["sales"],
    responses={401: {"description": "Invalid credentials"},
               404: {"description": "Not found"}},
)

logger = logging.getLogger(__name__)


@router.get("/", summary="Sales resource list",
            description="Get all sales items or a single by using query string `sale_id`. Supports `application/json` and `text/csv` as response type.",
            response_model=List[SaleDTOResponse] | SaleDTOResponse,)
async def list_sales(request: Request, db: Session = Depends(get_db), sale_id: int | None = None):
    if sale_id:
        prod = await find_sales_item(db, sale_id)

        if not prod:
            return Response(status_code=404)

        return prod

    return handle_csv_response(await find_sales_items(db, None, None), request, "sales_all")


@router.get("/year/{year}",
            summary="Get sales items by `year`",
            description="Get sales items by `year`",
            response_model=List[SaleDTOResponse])
async def list_sales_by_year(db: Session = Depends(get_db), year: int = None):
    return await find_sales_items(db, None, year)


@router.get("/category/{category}", summary="Sale resource list by category",
            description="Get sales items by `category`: tinto, branco, etc.",
            response_model=List[SaleDTOResponse])
async def list_sales_by_category(db: Session = Depends(get_db), category: str = None):
    return await find_sales_items(db, category, None)


@router.get("/category/{category}/year/{year}", summary="Sale resource list by category and year",
            description="Get sales items by `category` and `year`", response_model=List[SaleDTOResponse])
async def list_sales_by_category_and_year(db: Session = Depends(get_db), category: str = None, year: int = None):
    return await find_sales_items(db, category, year)


@router.post("/", summary="Sale resource add item",
             description="Protected resource that adds sales items to the dataset",
             response_model=SaleDTOResponse)
async def add_sales(current_user: Annotated[User, Depends(get_current_active_user)], dto: SaleDTO,
                         db: Session = Depends(get_db)):
    logger.warning(f'User {current_user.email} is adding a new sales item: {dto}')
    return sale_repository.create_new(db, dto)
