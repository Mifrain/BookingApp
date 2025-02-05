from sqlalchemy import select, or_, and_, func
from datetime import date

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms

from app.database import async_session_maker
from app.service.base import BaseService


class HotelService(BaseService):
    model = Hotels

    @classmethod
    async def find_all_free_hotels(cls, location: str, date_from: date, date_to: date):
        """
        WITH
-- отели
free_hotels AS (
    SELECT
        id AS hotel_id,
        name,
        location,
        rooms_quantity,
        image_id
    FROM hotels
    WHERE location LIKE '%Москва%'
),
-- забронированные комнаты
booked_rooms AS (
    SELECT * 
    FROM bookings
    WHERE
        (date_from >= '2023-05-30' AND date_from <= '2023-06-15') OR
        (date_from <= '2023-05-30' AND date_to > '2023-05-30')
),
-- Комнаты отелей
rooms_in_hotels AS (
    SELECT
        rooms.id AS room_id,
        rooms.hotel_id,
        rooms.quantity
    FROM rooms
    INNER JOIN free_hotels
    ON free_hotels.hotel_id = rooms.hotel_id
)

SELECT
    free_hotels.hotel_id,
    free_hotels.name,
    free_hotels.location,
    free_hotels.rooms_quantity,
    free_hotels.image_id,
    rooms_in_hotels.quantity - COUNT(booked_rooms.room_id) AS rooms_left
FROM free_hotels
LEFT JOIN rooms_in_hotels
ON rooms_in_hotels.hotel_id = free_hotels.hotel_id
LEFT JOIN booked_rooms
ON booked_rooms.room_id = rooms_in_hotels.room_id
GROUP BY
    free_hotels.hotel_id,
    free_hotels.name,
    free_hotels.location,
    free_hotels.rooms_quantity,
    free_hotels.image_id,
    rooms_in_hotels.quantity
HAVING
    rooms_in_hotels.quantity - COUNT(booked_rooms.room_id) > 0;
        """

        async with async_session_maker() as session:
            free_hotels = select(
                Hotels.id.label("hotel_id"),
                Hotels.name,
                Hotels.location,
                Hotels.rooms_quantity,
                Hotels.image_id,
            ).filter(Hotels.location.like(f"%{location}%")).cte("free_hotels")

            booked_rooms = select(
                Bookings.room_id,
            ).where(
                or_(
                    and_(
                        Bookings.date_from >= date_from,
                        Bookings.date_from <= date_to,
                    ),
                    and_(
                        Bookings.date_from <= date_from,
                        Bookings.date_to > date_from,
                    ),
                )
            ).cte("booked_rooms")

            rooms_in_hotels = select(
                Rooms.id.label("room_id"),
                Rooms.hotel_id,
                Rooms.quantity,
            ).join(
                free_hotels,
                free_hotels.c.hotel_id == Rooms.hotel_id,
            ).cte("rooms_in_hotels")

            get_hotels_left = select(
                free_hotels.c.hotel_id,
                free_hotels.c.name,
                free_hotels.c.location,
                free_hotels.c.rooms_quantity,
                free_hotels.c.image_id,
                (free_hotels.c.rooms_quantity - func.count(booked_rooms.c.room_id)).label(
                    "rooms_left"),
            ).select_from(
                free_hotels
            ).join(
                rooms_in_hotels,
                rooms_in_hotels.c.hotel_id == free_hotels.c.hotel_id,
                isouter=True,
            ).join(
                booked_rooms,
                booked_rooms.c.room_id == rooms_in_hotels.c.room_id,
                isouter=True,
            ).group_by(
                free_hotels.c.hotel_id,
                free_hotels.c.name,
                free_hotels.c.location,
                free_hotels.c.rooms_quantity,
                free_hotels.c.image_id,
            ).having(
                (free_hotels.c.rooms_quantity - func.count(booked_rooms.c.room_id)) > 0
            )

            hotels_left = await session.execute(get_hotels_left)
            hotels_left = hotels_left.mappings().all()
            return hotels_left

    @classmethod
    async def find_free_rooms_by_hotel(cls, hotel_id: int, date_from: date, date_to: date):
        ...