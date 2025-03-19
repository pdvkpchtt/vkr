from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import EmailStr
from fastapi import Request, HTTPException, Depends

from app.config import settings
from app.exceptions import NotFound, IncorrectEmailOrPasswordExceprion, TokenAbsentException, \
    IncorrectTokenFormatException, TokenExpireException, UserIsNotPresentException
from app.driverss.daos import AdminDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Для хеширования пароля
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

#Для проверки соответствия
def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

#Создание токена
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.key, settings.algoritm
    )
    return encoded_jwt

async def authenticate_user(email: EmailStr, password: str):
    user = await AdminDAO.find_one_or_none(email=email)
    if not user:
        raise NotFound
    if not verify_password(password, user.hashed_password):
        raise IncorrectEmailOrPasswordExceprion
    return user

def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.key, settings.algoritm
        )
    except JWTError:
        raise IncorrectTokenFormatException
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpireException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await AdminDAO.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user