from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.bookings.router import router as router_booking
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis

from app.config import settings

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

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding='utf8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")