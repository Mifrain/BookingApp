from datetime import date

from sqlalchemy import select, and_, or_, func, insert

from app.bookings.models import Bookings
from app.hotels.rooms.models import Rooms
from app.service.base import BaseService
from app.hotels.rooms.service import RoomService

from app.database import async_session_maker


class BookingService(BaseService):
    model = Bookings

    @classmethod
    async def add(cls, user_id: int, room_id:int, date_from: date, date_to: date):
        rooms_left = await RoomService.rooms_left(room_id, date_from, date_to)

        async with async_session_maker() as session:
            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()

                add_booking = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price= price
                ).returning(Bookings)

                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()