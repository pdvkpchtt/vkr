from app.DAO.base import BaseDAO
from app.database import async_session_factory
from app.driverss.schemas import SGetPartsBids
from app.models.models import Driver, Admins, Bid, Car, History, State
from sqlalchemy import update, select
from typing import List

class DriverDAO(BaseDAO):
    model = Driver

    @staticmethod
    async def update_password(email: str, password: str) -> None:
        async with async_session_factory() as session:
            query = update(Driver).where(Driver.email==email).values(hashed_password=password)
            await session.execute(query)
            await session.commit()

class BidDAO(BaseDAO):
    model = Bid

    @classmethod
    async def update_bid(cls, bid_id: int) -> None:
        async with async_session_factory() as session:
            query = update(cls.model).where(cls.model.id==bid_id).values(state=State.done)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def get_part_bids(cls, mechanic_id: int) -> List[SGetPartsBids]:
        async with async_session_factory() as session:
            query = (
                select(
                     Bid.id,
                     Bid.state,
                     Bid.description,
                     Bid.date,
                )
                .select_from(Bid)
                .where(Bid.mechanic_id == mechanic_id)
            )
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def get_part_state(cls, bid_id: int) -> List[SGetPartsBids]:
        async with async_session_factory() as session:
            query = (
                select(
                    Bid.state,
                )
                .select_from(Bid)
                .where(Bid.id == bid_id)
            )
            result = await session.execute(query)
            return result.mappings().one_or_none()

class AdminDAO(BaseDAO):
    model = Admins

class CarDAO(BaseDAO):
    model = Car

class HistoryDAO(BaseDAO):
    model = History
