from datetime import datetime

from app.bookings.service import BookingService

async def test_ass_and_get_booking():
    new_booking = await BookingService.add(
        user_id=1,
        room_id=2,
        date_from=datetime.strptime("2024-07-10", "%Y-%m-%d"),
        date_to=datetime.strptime("2024-07-24", "%Y-%m-%d"),
    )

    new_booking = await BookingService.find_by_id(new_booking.id)

    assert new_booking is not None