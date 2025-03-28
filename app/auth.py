from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import EmailStr
from fastapi import Request, Depends

from app.config import settings
from app.database import Base
from app.exceptions import NotFound, IncorrectEmailOrPasswordExceprion, TokenAbsentException, \
    IncorrectTokenFormatException, TokenExpireException, UserIsNotPresentException
from app.driverss.daos import AdminDAO, DriverDAO
from app.mechanic.dao import MechanicDAO
from app.models.models import Admins, Driver, Mechanic

# mypy: ignore-errors

class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # Для хеширования пароля
    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls.pwd_context.hash(password)

    # Для проверки соответствия
    @classmethod
    def verify_password(cls, plain_password, hashed_password) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)

    # Создание токена
    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=30)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.key, settings.algoritm
        )
        return encoded_jwt

    @classmethod
    async def authenticate_user(
            cls,
            email: EmailStr,
            password: str,
            dao: [MechanicDAO | DriverDAO | AdminDAO]
    ) -> Mechanic | Driver | Admins:
        user = await dao.find_one_or_none(email=email)
        if not user:
            raise NotFound
        if not cls.verify_password(password, user.hashed_password):
            raise IncorrectEmailOrPasswordExceprion
        return user

    @staticmethod
    def get_token(request: Request):
        token = request.cookies.get("app_token")
        if not token:
            raise TokenAbsentException
        return token

    @staticmethod
    async def get_current_user(token: str = Depends(get_token)) -> Admins | Driver | Mechanic:
        try:
            payload = jwt.decode(
                token, settings.key, settings.algoritm
            )
        except JWTError:
            raise IncorrectTokenFormatException
        expire: str = payload.get("exp")
        if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
            raise TokenExpireException
        user_type: str = payload.get("type")
        if not user_type:
            raise UserIsNotPresentException
        if user_type == "driver":
            user_type_dao = DriverDAO
        elif user_type == "mechanic":
            user_type_dao = MechanicDAO
        else:
            user_type_dao = AdminDAO
        user_id: str = payload.get("sub")
        if not user_id:
            raise UserIsNotPresentException
        user = await user_type_dao.find_by_id(int(user_id))
        if not user:
            raise UserIsNotPresentException
        return user

    @staticmethod
    def check_type_admin(admin: Base) -> None:
        if not (isinstance(admin, Admins)):
            raise UserIsNotPresentException

    @staticmethod
    def check_type_driver(driver: Base) -> None:
        if not (isinstance(driver, Driver)):
            raise UserIsNotPresentException

    @staticmethod
    def check_type_mechanic(mechanic: Base) -> None:
        if not (isinstance(mechanic, Mechanic)):
            raise UserIsNotPresentException

    @staticmethod
    def check_type_mechanic_or_driver(model: Base) -> None:
        if not (isinstance(model, Mechanic)) and not (isinstance(model, Driver)):
            raise UserIsNotPresentException
