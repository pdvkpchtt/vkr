from app.DAO.base import BaseDAO
from app.database import async_session_factory
from app.models.models import Mechanic
from sqlalchemy import update
class MechanicDAO(BaseDAO):
    model = Mechanic
    @staticmethod
    async def update_password(email: str, password: str) -> None:
        async with async_session_factory() as session:
            query = update(Mechanic).where(Mechanic.email==email).values(hashed_password=password)
            await session.execute(query)
            await session.commit()
