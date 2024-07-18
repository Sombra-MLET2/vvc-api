import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dtos import CategoryDTO, CategoryWithIdDTO
from infra.database.database import get_db
from infra.security.security import get_current_active_user
from ucs.categories import list_all_categories

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    dependencies=[Depends(get_current_active_user)],
    responses={401: {"description": "Invalid credentials"},
               404: {"description": "Not found"}},
)

logger = logging.getLogger(__name__)


@router.get("/", summary="Categories resource list",
            description="List all categories available in this dataset.",
            response_model=List[CategoryWithIdDTO])
async def list_categories(db: Session = Depends(get_db)):
    return list_all_categories(db)


@router.post("/", summary="Categories resource create", description="Create a new category to be used in this dataset",
             response_model=CategoryWithIdDTO)
async def add_category(db: Session = Depends(get_db), cat: CategoryDTO | None = None):
    raise HTTPException(
        status_code=501,
        detail="This endpoint has not been implemented yet."
    )
