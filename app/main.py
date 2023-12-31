from fastapi import FastAPI
from app.utils.dependencies import get_db_session, close_db_session
from app.utils.schedule import SchedulerService
from fastapi import Depends
from app.db.db import AsyncSession

from .routers import users, auth, companies, quizzes, analitics, notifications

app = FastAPI()


@app.on_event("startup")
async def connect_db():
    get_db_session()
    SchedulerService()


@app.on_event("shutdown")
async def disconnect_db():
    await close_db_session()


@app.get("/")
async def health_check():
    return {"status_code": 200, "detail": "ok", "result": "working"}


app.include_router(users.router)
app.include_router(auth.router)
app.include_router(companies.router)
app.include_router(quizzes.router)
app.include_router(analitics.router)
app.include_router(notifications.router)
