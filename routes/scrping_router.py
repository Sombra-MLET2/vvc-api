import logging
from fastapi import APIRouter, Depends, HTTPException
from scraping.scraping import *


router = APIRouter(
    prefix="/scraping",
    tags=["scraping"],
    responses={401: {"description": "Invalid credentials"},
               404: {"description": "Not found"},
               409: {"description": "Invalid user creation request"}},
)

logger = logging.getLogger(__name__)


@router.get("/map_site")
async def map_all_site():
    return map_site()


@router.get("/download_all_csv")
async def download_all_csv_site():
    return download_all_csv()
