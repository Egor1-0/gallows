import os
from dotenv import load_dotenv
from sqlalchemy import String, BigInteger, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

load_dotenv()

engine = create_async_engine(url=os.getenv('DB_URL'))

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Session(Base):
    __tablename__ = 'sessions'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    original_word: Mapped[str] = mapped_column(String(10))
    guess_word: Mapped[str] = mapped_column(String(10))
    used_letters: Mapped[str] = mapped_column(String(33), default='')
    lifes: Mapped[int] = mapped_column(default=7)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)