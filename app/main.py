from fastapi import FastAPI

from app.bookings.router import router as router_booking
from app.users.router import router as router_users

app = FastAPI()


app.include_router(router_users)
app.include_router(router_booking)
