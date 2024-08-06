import logging
from fastapi import APIRouter
from scraping.scraping import map_site, download_all_csv

router = APIRouter(
    prefix="/scraping",
    tags=["scraping"],
    responses={401: {"description": "Invalid credentials"},
               404: {"description": "Not found"},
               409: {"description": "Invalid user creation request"}}
)

logger = logging.getLogger(__name__)


@router.post("map_site")
async def set_map_site():
    """
        Returns the site structure
    """
    return map_site()


@router.get("/download_all_csv")
async def download_all_csv_site():
    """
         Download all csv files found on the site
    """
    return download_all_csv()
