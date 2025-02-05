from datetime import date
from fastapi import APIRouter

from app.hotels.schemas import SHotels
from app.hotels.service import HotelService

router = APIRouter(
    prefix="/hotels",
    tags=["Отели и Комнаты"],
)

@router.get('')
def all_hotels():
    ...


@router.get('/{location}')
async def find_hotels(location: str, date_from: date, date_to: date):
    return await HotelService.find_all_free_hotels(location=location, date_from=date_from, date_to=date_to)