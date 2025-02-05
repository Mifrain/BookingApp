from datetime import date
from fastapi import APIRouter
from fastapi_cache.decorator import cache


from app.hotels.schemas import SHotels
from app.hotels.service import HotelService

router = APIRouter(
    prefix="/hotels",
    tags=["Отели и Комнаты"],
)


# TODO: Получение списка комнат, Получение списка бронирований, Удаление бронирования

@router.get('')
def all_hotels():
    ...


@router.get('/{location}')
@cache(expire=60)
async def find_hotels(location: str, date_from: date, date_to: date):
    return await HotelService.find_all_free_hotels(location=location, date_from=date_from, date_to=date_to)