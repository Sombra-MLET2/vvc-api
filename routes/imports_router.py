import logging
from typing import Annotated, List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import Response

from dtos import ImportDTOResponse, ImportDTO
from infra.converter.fast_api_csv_converter import handle_csv_response
from infra.database.database import get_db
from infra.security.security import get_current_active_user
from models.user import User
from ucs.imports import find_imports_item, find_imports_items, add_import_item

router = APIRouter(
    prefix="/imports",
    tags=["imports"],
    responses={401: {"description": "Invalid credentials"},
               404: {"description": "Not found"}},
)

logger = logging.getLogger(__name__)


@router.get("/", summary="Import resource list",
            description="Get all import items or a single by using query string `imp_id`. Supports `application/json` and `text/csv` as response type.",
            response_model=List[ImportDTOResponse] | ImportDTOResponse,)
async def list_imports(request: Request, db: Session = Depends(get_db), imp_id: int | None = None):
    if imp_id:
        prod = await find_imports_item(db, imp_id)

        if not prod:
            return Response(status_code=404)

        return prod

    return handle_csv_response(await find_imports_items(db, None, None, None), request, "imports_all")


@router.get("/year/{year}",
            summary="Get imports items by `year`",
            description="Get imports items by `year`",
            response_model=List[ImportDTOResponse])
async def list_imports_by_year(db: Session = Depends(get_db), year: int = None):
    return await find_imports_items(db, None, year, None)


@router.get("/category/{category}", summary="Import resource list by category",
            description="Get imports items by `category`: tinto, branco, etc.",
            response_model=List[ImportDTOResponse])
async def list_imports_by_category(db: Session = Depends(get_db), category: str = None):
    return await find_imports_items(db, category, None, None)


@router.get("/country/{country}", summary="Import resource list by country",
            description="Get imports items by `country`: Brasil, Chile, etc.",
            response_model=List[ImportDTOResponse])
async def list_imports_by_category(db: Session = Depends(get_db), country: str = None):
    return await find_imports_items(db, None, None, country)


@router.get("/category/{category}/year/{year}", summary="Import resource list by category and year",
            description="Get imports items by `category` and `year`", response_model=List[ImportDTOResponse])
async def list_imports_by_category_and_year(db: Session = Depends(get_db), category: str = None, year: int = None):
    return await find_imports_items(db, category, year, None)


@router.get("/country/{country}/year/{year}", summary="Import resource list by country and year",
            description="Get imports items by `country` and `year`",
            response_model=List[ImportDTOResponse])
async def list_imports_by_category(db: Session = Depends(get_db), country: str = None, year: str = None):
    return await find_imports_items(db, None, year, country)


@router.post("/", summary="Import resource add item",
             description="Protected resource that adds imports items to the dataset",
             response_model=ImportDTOResponse)
async def add_imports(current_user: Annotated[User, Depends(get_current_active_user)], dto: ImportDTO,
                         db: Session = Depends(get_db)):
    logger.warning(f'User {current_user.email} is adding a new imports item: {dto}')
    return add_import_item(db, dto)
