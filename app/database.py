from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import NullPool

from app.config import settings

if settings.MODE == "TEST":
    DATABASE_URL = settings.DATABASE_URL_asyncpg_test
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL_asyncpg
    DATABASE_PARAMS = {}

engine = create_async_engine(url=DATABASE_URL, **DATABASE_PARAMS)

async_session_factory = async_sessionmaker(engine)

class Base(DeclarativeBase):
    __abstract__ = True
    __table_args__ = {'extend_existing': True}


