from app.database.models import async_session, Session
from sqlalchemy import select

async def set_word(tg_id, word):
    async with async_session() as session:
        session.add(Session(tg_id = tg_id, original_word = word, guess_word = '_'*len(word)))
        await session.commit()

async def update_guess_word(tg_id, letter, word):
    async with async_session() as session:
        data = await session.scalar(select(Session).where(Session.tg_id == tg_id))
        for i in range(len(word) - 1):
            if word[i] == letter:
                data.guess_word = data.guess_word[:i] + letter + data.guess_word[i + 1:] 
        if word[-1] == letter:
            data.guess_word = data.guess_word[:-1] + letter
        await session.commit()

async def auto_decriment_lifes(tg_id):
    async with async_session() as session:
        data = await session.scalar(select(Session).where(Session.tg_id == tg_id))
        data.lifes -= 1
        await session.commit()