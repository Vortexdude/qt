from fastapi import APIRouter
from api.utils.main import NetflixDataScraper

router = APIRouter()


@router.get("/")
async def get_nt_data():
    nt = NetflixDataScraper()
    nt.get_data()
    return nt.data
