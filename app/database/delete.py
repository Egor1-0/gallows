from app.database.models.models import Session
from app.database.models.session import async_session
from sqlalchemy import delete

async def delete_session(tg_id):
    async with async_session() as session:
        await session.execute(delete(Session).where(Session.tg_id == tg_id))
        await session.commit()