from app.db.db import async_session, AsyncSession, r
import asyncio


async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        except asyncio.exceptions.CancelledError:
            await session.close()


async def close_db_session():
    await r.close()
