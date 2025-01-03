from sqlalchemy import select

from app.bookings.models import Bookings
from app.service.base import BaseService

from app.database import async_session_maker


class BookingService(BaseService):
    model = Bookings
