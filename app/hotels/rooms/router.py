from app.hotels.router import router


@router.get('/{hotel_id}/rooms')
def all_rooms():
    ...