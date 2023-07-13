from fastapi import FastAPI
from .db.db import async_session, AsyncSession, r

app = FastAPI()

@app.on_event("startup")
async def get_db_session() -> AsyncSession:
    async with async_session as session:
        yield session

@app.on_event("shutdown")
async def close_db_session():
    r.close()



@app.get("/")
def health_check():
    return {
        "status_code": 200,
        "detail": "ok",
        "result": "working"
    }
