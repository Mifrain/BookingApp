from datetime import date

from fastapi import  APIRouter, Depends
from pydantic import parse_obj_as

from app.bookings.schemas import SBooking
from app.bookings.service import BookingService
from app.exceptions import RoomCannotBeBooked
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix='/bookings',
    tags=["Бронирования"],
)

@router.get("/")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingService.find_all(user_id=user.id)


@router.post("/")
async def add_booking(
        room_id:int, date_from: date, date_to: date,
        user: Users = Depends(get_current_user)
):
    booking = await BookingService.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
    booking_dict = parse_obj_as(SBooking, booking).dict()
    send_booking_confirmation_email.delay(booking_dict, user.email)
    return booking
