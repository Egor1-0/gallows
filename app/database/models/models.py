from sqlalchemy import String, BigInteger, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs



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

