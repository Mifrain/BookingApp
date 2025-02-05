from fastapi import APIRouter, Response, Depends

from app.exceptions import UserAlreadyExistsException, IncorrectCreditalsException
from app.users.auth import get_password_hash, verify_password, authenticate_user, create_access_token
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth
from app.users.services import UserService

router = APIRouter(
    prefix='/auth',
    tags=['Auth & Users']
)


@router.post('/register')
async def register_user(user_data: SUserAuth):
    existing_user = await UserService.find_one_or_none(email = user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UserService.add(email=user_data.email, hashed_password=hashed_password)

@router.post('/login')
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectCreditalsException

    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie('booking_access_token', access_token, httponly=True)
    return access_token

@router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")

@router.get('/me')
async def about_me(user: Users = Depends(get_current_user)):
    return user
