import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import Response

from dtos import ProcessingDTO, ProcessingDTOResponse
from infra.converter.fast_api_csv_converter import handle_csv_response
from infra.database.database import get_db
from infra.security.security import get_current_active_user
from models.user import User
from ucs.processing import find_processing_item, find_processing_items, add_new_processing_item

router = APIRouter(
    prefix="/processing",
    tags=["processing"],
    responses={401: {"description": "Invalid credentials"},
               404: {"description": "Not found"}},
)

logger = logging.getLogger(__name__)


@router.get("/", summary="Processing resource list",
            description="Get all processing items or a single by using query string `proc_id`",
            response_model=List[ProcessingDTOResponse] | ProcessingDTOResponse)
async def list_processing(request: Request, db: Session = Depends(get_db), proc_id: int | None = None):
    if proc_id:
        proc = await find_processing_item(db, proc_id)

        if not proc:
            return Response(status_code=404)

        return proc

    return handle_csv_response(await find_processing_items(db, None, None, None), request, "processing_all")


@router.get("/year/{year}", summary="Processing resource list by year", description="Get processing items by `year`",
            response_model=List[ProcessingDTOResponse])
async def list_processing_by_year(db: Session = Depends(get_db), year: int = None):
    return await find_processing_items(db, None, year, None)


@router.get("/category/{category}", summary="Processing resource list by category",
            description="Get processing items by `category`: tinto, branco, etc.",
            response_model=List[ProcessingDTOResponse])
async def list_processing_by_category(db: Session = Depends(get_db), category: str = None):
    return await find_processing_items(db, category, None, None)


@router.get("/grape/{grape}", summary="Processing resource list by grape class",
            description="Get processing items by `grape class`: mesa, hibrida, americana, etc.",
            response_model=List[ProcessingDTOResponse])
async def list_processing_by_category(db: Session = Depends(get_db), grape: str = None):
    return await find_processing_items(db, None, None, grape)


@router.get("/grape/{grape}/year/{year}", summary="Processing resource list by grape class and year",
            description="Get processing items by `grape class` and `year`.", response_model=List[ProcessingDTOResponse])
async def list_processing_by_category(db: Session = Depends(get_db), grape: str = None, year: int = None):
    return await find_processing_items(db, None, year, grape)


@router.get("/category/{category}/year/{year}", summary="Processing resource list by category and year",
            description="Get processing items by `category` and `year`", response_model=List[ProcessingDTOResponse])
async def list_processing_by_category_year(db: Session = Depends(get_db), category: str = None, year: int = None):
    return await find_processing_items(db, category, year, None)


@router.post("/", summary="Processing resource add item",
             description="Protected resource that adds processing items to the dataset",
             response_model=ProcessingDTOResponse)
async def add_processing(current_user: Annotated[User, Depends(get_current_active_user)], dto: ProcessingDTO,
                         db: Session = Depends(get_db)):
    logger.warning(f'User {current_user.email} is adding a new processing item: {dto}')
    return add_new_processing_item(db, dto)
