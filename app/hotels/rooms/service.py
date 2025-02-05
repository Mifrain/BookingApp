from sqlalchemy import select, and_, or_, func
from datetime import date

from app.database import async_session_maker
from app.bookings.models import Bookings
from app.hotels.rooms.models import Rooms
from app.service.base import BaseService



class RoomService(BaseService):
    model = Rooms

    @classmethod
    async def rooms_left(cls, room_id:int, date_from: date, date_to: date):

        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == room_id,
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to,
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from,
                        )
                    )
                )
            ).cte("booked rooms")

            get_rooms_left = select(
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left")
            ).select_from(Rooms).join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
            ).where(Rooms.id == room_id).group_by(
                Rooms.quantity, booked_rooms.c.room_id
            )

            rooms_left = await session.execute(get_rooms_left)
            rooms_left: int = rooms_left.scalar()

            return rooms_left