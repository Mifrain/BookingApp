from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.bookings.router import router as router_booking
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels

app = FastAPI()


app.include_router(router_users)
app.include_router(router_booking)
app.include_router(router_hotels)

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)