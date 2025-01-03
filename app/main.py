from fastapi import FastAPI

from app.bookings.router import router as router_booking

app = FastAPI()

app.include_router(router_booking)
