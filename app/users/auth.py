from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

from app.users.services import UserService
from app.config import settings


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM
    )
    return encoded_jwt


async def authenticate_user(email: str, password: str):
    user = await UserService.find_one_or_none(email=email)
    if not user and not verify_password(password, user.hashed_password):
        return None
    return user

# TODO: add refresh_access_token