from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import create_engine
import os
import logging

sync_engine = create_engine(
    os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/space-catalogue")
        .replace("+asyncpg", "")
)

def database_init(database_url=None):
    if database_url is None:
        database_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@db:5432/space-catalogue")
    engine = create_async_engine(database_url)
    SessionLocal = async_sessionmaker(engine)
    return engine, SessionLocal

engine, SessionLocal = database_init()

async def get_db_conn():
    async with engine.begin() as conn:
        yield conn

def get_logger():
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(__name__)