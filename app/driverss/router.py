
from fastapi import APIRouter, BackgroundTasks, Response, Depends
from typing import List
from app.auth import Auth
from app.controller.controller_driver import mechanic_assigner
# from app.driver.dao import DriverDAO, Driver
from app.driverss.daos import BidDAO, HistoryDAO, DriverDAO, CarDAO
from app.driverss.schemas import SUserAuth, SGetStatusBid, SGetHistory, SGetBid, SGetBidsForDriverWithInfoMechanic
from app.exceptions import NotFound, UserAlreadyExistException
from app.mechanic.dao import MechanicDAO
from app.models.models import State, Driver
from app.tasks.tasks import send_mechanic_confirmation_email

router = APIRouter(
    prefix="/driver",
    tags=["Водитель"]
)

# ручка по добавлению водителями заявки на ремонт авто
@router.post("/create_bid", response_model=str)
async def add_bid(
    description: str,
    background_tasks: BackgroundTasks,
    driver: Driver = Depends(Auth.get_current_user)
) -> str:
    Auth.check_type_driver(driver)

    mechanics = await MechanicDAO.find_all()

    if not mechanics:
        raise ValueError("Нет доступных механиков")

    # Выбираем механика по индексу
    selected_mechanic = await mechanic_assigner.get_next_mechanic(mechanics)

    await BidDAO.add(
        description = description,
        state = State.procces,
        driver_id = driver.id,
        mechanic_id = selected_mechanic,
    )
    # Отправка на почту письма
    res = await MechanicDAO.find_by_id(model_id=selected_mechanic)
    background_tasks.add_task(send_mechanic_confirmation_email,description, res.email)
    return "Заявка создана. Информация о заявке отправлена на почту механику"

# ручка на просмотр всех заявок
@router.get("/bids", response_model=List[SGetBid])
async def get_driver_bids(
    driver: Driver = Depends(Auth.get_current_user)
):
    Auth.check_type_driver(driver)
    res = await BidDAO.find_all(driver_id=driver.id)
    return res


#!!!!!!!!!!
# ручка на получение дополнительной инофрмации об исполнителе
@router.get("/get_info_bids_of_mechanic", response_model=SGetBidsForDriverWithInfoMechanic) #, response_model=SGetStatusBid
async def get_status_bid(
    bid_id: int,
    driver: Driver = Depends(Auth.get_current_user)

):
    Auth.check_type_driver(driver)
    bid_info = await BidDAO.find_one_or_none(id=bid_id)
    info_mechanic = await MechanicDAO.find_one_or_none(id=bid_info.mechanic_id)
    if not bid_info or not info_mechanic:
        raise NotFound
    return {
            "info_bid": bid_info,
            "info_mechanic": info_mechanic,
            }


# @router.get("/get_history_bids", response_model=List[SGetHistory])
# async def get_history(
#     driver: Driver = Depends(Auth.get_current_user)
# ):
#     Auth.check_type_driver(driver)
#     res = await HistoryDAO.find_all(car_id=driver.car_id)
#     return res

# ручка на проверки авто
@router.get("/get_info_auto")
async def get_info_auto(
    driver: Driver = Depends(Auth.get_current_user)
):
    Auth.check_type_driver(driver)
    res = await CarDAO.find_one_or_none(id=driver.car_id)
    return res

@router.get("/get_history_auto")
async def get_info_auto(
    driver: Driver = Depends(Auth.get_current_user)
):
    Auth.check_type_driver(driver)
    res = await HistoryDAO.find_all(car_id=driver.car_id)
    return res

# ручка на регистрацию
@router.post("/register", response_model=str)
async def register_driver(
    user_data: SUserAuth
):
    existing_user = await DriverDAO.find_one_or_none(email=user_data.email)
    if existing_user is None:
        raise NotFound
    if existing_user.hashed_password is not None:
        raise UserAlreadyExistException
    hashed_password = Auth.get_password_hash(user_data.password)
    await DriverDAO.update_password(email=user_data.email, password=hashed_password)
    return "Регистрация прошла успешно!"

@router.post("/login")
async def login(
    response: Response,
    user_data: SUserAuth
):
    user = await Auth.authenticate_user(email=user_data.email, password=user_data.password, dao=DriverDAO)
    access_token = Auth.create_access_token({"sub": str(user.id), "type": "driver"})  #передаём строку
    response.set_cookie("app_token", access_token, httponly=True)
    return access_token
