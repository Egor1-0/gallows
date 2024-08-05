from app.database.models.models import Session
from app.database.models.session import async_session
from sqlalchemy import select
async def get_row(tg_id):
    async with async_session() as session:
        return await session.scalar(select(Session).where(Session.tg_id == tg_id))

async def get_lifes(tg_id):
    async with async_session() as session:
        return (await session.scalar(select(Session).where(Session.tg_id == tg_id))).lifes

async def get_used_letters(tg_id):
    async with async_session() as session:
        return (await session.scalar(select(Session).where(Session.tg_id == tg_id))).used_letters

async def get_guess_word(tg_id):
    async with async_session() as session:
        return (await session.scalar(select(Session).where(Session.tg_id == tg_id))).guess_word

async def is_win(tg_id):
    async with async_session() as session:
        data = await session.scalar(select(Session).where(Session.tg_id == tg_id))
        return data.guess_word == data.original_word

async def is_lose(tg_id):
    async with async_session() as session:
        data = await session.scalar(select(Session).where(Session.tg_id == tg_id))
        return data.lifes == 0