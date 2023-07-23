from app.db.db import async_session, AsyncSession, r

async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        yield session

async def close_db_session():
    await r.close()