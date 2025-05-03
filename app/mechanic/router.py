from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Response, Depends, BackgroundTasks

from app.auth import Auth
from app.driverss.schemas import SUserAuth, SGetPartsBids, SGetBid
from app.exceptions import NotFound, UserAlreadyExistException
from app.mechanic.dao import MechanicDAO
from app.models.models import Mechanic
from app.driverss.daos import BidDAO, DriverDAO, HistoryDAO, CarDAO
from app.tasks.tasks import send_driver_confirmation_email

router = APIRouter(
    prefix="/mechanic",
    tags=["Механик"]
)

# ручка по добавлению механиками истории обслуживания и измненению bid
@router.post("/add_history", response_model=str)
async def add_history(
    bid_id: int,
    run: int,
    description: str,
    work_hours: float,
    spares: str,
    background_tasks: BackgroundTasks,
    mechanic: Mechanic = Depends(Auth.get_current_user),
):
    Auth.check_type_mechanic(mechanic)
    bid =  await BidDAO.find_one_or_none(id=bid_id)
    driver = await DriverDAO.find_one_or_none(id=bid.driver_id)
    if not bid or not driver:
        raise NotFound

    await BidDAO.update_bid(bid_id)
    data = datetime.now(timezone.utc)
    await HistoryDAO.add(
        date=data,
        run=run,
        description=description,
        mechanic_id=mechanic.id,
        car_id=driver.car_id,
        work_hours=work_hours,
        spares=spares,
    )
    # Отправка на почту письма
    background_tasks.add_task(send_driver_confirmation_email,bid_id, description, driver.email)
    return "Данные отправлены. Информация о заявке отправлена на почту водителю"

# Ручка просмотра частичных данных тасок
@router.get("/bids", response_model=List[SGetPartsBids])
async def get_bids(
    mechanic: Mechanic = Depends(Auth.get_current_user),
):
    Auth.check_type_mechanic(mechanic)
    result = await BidDAO.get_part_bids(mechanic_id=mechanic.id)
    return result


#!!!!!!!!!!
# Ручка просмотра таски
@router.get("/bids/{bid_id}") #, response_model=SGetBid
async def get_bid_id(
    bid_id: int,
    mechanic: Mechanic = Depends(Auth.get_current_user),
):
    Auth.check_type_mechanic(mechanic)
    bib_res = await BidDAO.find_one_or_none(id=bid_id)
    driver_res = await DriverDAO.find_one_or_none(id=bib_res.driver_id)
    car_res = await CarDAO.find_one_or_none(id=driver_res.car_id)
    return {"bid":bib_res,
            "driver": driver_res,
            "car": car_res,
            }

# ручка на регистрацию
@router.post("/register")
async def register_driver(
    user_data: SUserAuth
):
    existing_user = await MechanicDAO.find_one_or_none(email=user_data.email)
    if existing_user is None:
        raise NotFound
    if existing_user.hashed_password is not None:
        raise UserAlreadyExistException
    hashed_password = Auth.get_password_hash(user_data.password)
    await MechanicDAO.update_password(email=user_data.email, password=hashed_password)
    return "Регистрация прошла успешно!"

@router.post("/login")
async def login(
    response: Response,
    user_data: SUserAuth
):
    user = await Auth.authenticate_user(user_data.email, user_data.password, MechanicDAO)
    access_token = Auth.create_access_token({"sub": str(user.id), "type": "mechanic"})  #передаём строку
    response.set_cookie("app_token", access_token, httponly=True)
    return access_token
