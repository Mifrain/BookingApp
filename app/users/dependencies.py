from datetime import datetime

from fastapi import Request, HTTPException, Depends, status
from jose import jwt, JWTError

from app.config import settings
from app.users.models import Users
from app.users.services import UserService


# Получение токена во время запроса к беку
def get_token(request: Request):
    token = request.cookies.get('booking_access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token

# Проверка JWT
# 1) проверить правильный ли стиль JWT
# 2) Проверить дату окончания токена
# 3) Проверка ключа
async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # Дата окончания токена
    expire: str = payload.get('exp')
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # Получения id
    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # Получение пользователя
    user: Users = await UserService.find_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user