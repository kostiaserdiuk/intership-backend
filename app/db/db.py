from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from redis import asyncio as aioredis

from dotenv import load_dotenv
from os import getenv

load_dotenv()

user = getenv("POSTGRES_USER")
password = getenv("POSTGRES_PASSWORD")
db = getenv("POSTGRES_DB")
postgres_host = getenv("POSTGRES_HOST")
postgres_port = getenv("POSTGRES_PORT")


DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@{postgres_host}:{postgres_port}/{db}"

engine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, autoflush=False, class_=AsyncSession)
Base = declarative_base()

r = aioredis.from_url(f"redis://intership-backend-redis-1", encoding="utf-8", decode_responses=True)