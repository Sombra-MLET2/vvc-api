import logging
from typing import Annotated, List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import Response

from dtos import ExportDTO, ExportDTOResponse
from infra.converter.fast_api_csv_converter import handle_csv_response
from infra.database.database import get_db
from infra.security.security import get_current_active_user
from models.user import User
from ucs.exports import find_exports_item, find_exports_items, add_export_item

router = APIRouter(
    prefix="/exports",
    tags=["exports"],
    responses={401: {"description": "Invalid credentials"},
               404: {"description": "Not found"}},
)

logger = logging.getLogger(__name__)


@router.get("/", summary="Export resource list",
            description="Get all export items or a single by using query string `exp_id`. Supports `application/json` and `text/csv` as response type.",
            response_model=List[ExportDTOResponse] | ExportDTOResponse,)
async def list_exports(request: Request, db: Session = Depends(get_db), exp_id: int | None = None):
    if exp_id:
        prod = find_exports_item(db, exp_id)

        if not prod:
            return Response(status_code=404)

        return prod

    return handle_csv_response(find_exports_items(db, None, None, None), request, "exports_all")


@router.get("/year/{year}",
            summary="Get exports items by `year`",
            description="Get exports items by `year`",
            response_model=List[ExportDTOResponse])
async def list_exports_by_year(db: Session = Depends(get_db), year: int = None):
    return find_exports_items(db, None, year, None)


@router.get("/category/{category}", summary="Export resource list by category",
            description="Get exports items by `category`: tinto, branco, etc.",
            response_model=List[ExportDTOResponse])
async def list_exports_by_category(db: Session = Depends(get_db), category: str = None):
    return find_exports_items(db, category, None, None)


@router.get("/country/{country}", summary="Export resource list by country",
            description="Get exports items by `country`: Brasil, Chile, etc.",
            response_model=List[ExportDTOResponse])
async def list_exports_by_category(db: Session = Depends(get_db), country: str = None):
    return find_exports_items(db, None, None, country)


@router.get("/category/{category}/year/{year}", summary="Export resource list by category and year",
            description="Get exports items by `category` and `year`", response_model=List[ExportDTOResponse])
async def list_exports_by_category_and_year(db: Session = Depends(get_db), category: str = None, year: int = None):
    return find_exports_items(db, category, year, None)


@router.get("/country/{country}/year/{year}", summary="Export resource list by country and year",
            description="Get exports items by `country` and `year`",
            response_model=List[ExportDTOResponse])
async def list_exports_by_category(db: Session = Depends(get_db), country: str = None, year: str = None):
    return find_exports_items(db, None, year, country)


@router.post("/", summary="Export resource add item",
             description="Protected resource that adds exports items to the dataset",
             response_model=ExportDTOResponse)
async def add_exports(current_user: Annotated[User, Depends(get_current_active_user)], dto: ExportDTO,
                         db: Session = Depends(get_db)):
    logger.warning(f'User {current_user.email} is adding a new exports item: {dto}')
    return add_export_item(db, dto)
