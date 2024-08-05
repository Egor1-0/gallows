import os
from dotenv import load_dotenv

from app.database.models.models import Base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

load_dotenv()

engine = create_async_engine(url=os.getenv('DB_URL'))

async_session = async_sessionmaker(engine)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)