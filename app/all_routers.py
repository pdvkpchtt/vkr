from typing import Optional

from fastapi import APIRouter, Response, Depends
from app.database import Base
from app.auth import Auth
from app.driverss.schemas import SDriver, SMechanic

router = APIRouter(
    prefix="/all",
    tags=["Выход и информация о себе"]
)

@router.post("/logout")
async def logout_user(response: Response) -> None:
    response.delete_cookie("app_token")

@router.get("/me", response_model=Optional[SDriver | SMechanic])
async def read_users_me(
        user: Base = Depends(Auth.get_current_user)
):
    role = Auth.check_type_mechanic_or_driver(user)

    user.role = role

    return user
