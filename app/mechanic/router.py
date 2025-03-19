from fastapi import APIRouter

from app.DAO.base import BaseDAO
from app.driverss.daos import BidDAO
from app.mechanic.dao import MechanicDAO

router = APIRouter(
    prefix="/driver",
)

# # ручка по добавлению механиками истории обслуживания
# @router.post("")
# async def add_history(
#     car_id: int,
#     description: str,
#     mechanic_id: int,
# ):
#     await F("54")
#
# async def F(car: int): ...


# ручка по измненению bid
@router.post("")
async def done_task(
    bid_id,
    car_id: int,
    description: str,
    status: str,
    run: str,
    mechanic_id: int,
): ...

# Ручка просмотра тасок
@router.get("/bids")
async def get_bids(
    mechanic_id: int = 1
):
    result = await BidDAO.find_all(mechanic_id=mechanic_id)
    return result