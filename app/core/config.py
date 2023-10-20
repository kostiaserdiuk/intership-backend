import os

import dotenv

dotenv.load_dotenv()


POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT: str = os.environ.get("POSTGRES_PORT")
POSTGRES_DB: str = os.environ.get("POSTGRES_DB")
POSTGRES_USER: str = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD")

REDIS_HOST: str = os.environ.get("REDIS_HOST")
REDIS_PORT: str = os.environ.get("REDIS_PORT")
