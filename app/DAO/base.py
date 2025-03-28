from typing import Type

from sqlalchemy import select, insert


from app.database import async_session_factory


# mypy: ignore-errors


class BaseDAO():
    model: Type[object] | None = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_factory() as session: # noqa: F811
            query = select(cls.model).filter_by(id=model_id) # noqa
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_factory() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by) #model_id=2, price=133
            result = await session.execute(query)
            return result.mappings().one_or_none()
            # return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_factory() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **data) -> None:
        async with async_session_factory() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    # @classmethod
    # async def delete_one_bookings(cls, booking_id, user):
    #     async with async_session_factory() as session:
    #         query = delete(cls.model).where(cls.model.id == booking_id, cls.model.user_id == user)
    #         result = await session.execute(query)
    #         await session.commit()
    #         return result

    # @classmethod
    # async def find_all(cls):
    #     async with async_session_factory() as session:
    #         query = select(cls.model)
    #         result = await session.execute(query)
    #         return result.scalars().all()
