from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials
from sqlalchemy import select
from datetime import datetime, timedelta
from app.utils.utils import VerifyToken
import jwt


import os
from dotenv import load_dotenv

from app.schemas.schemas import User
from app.db.db import AsyncSession
from app.models.models import User as UserModel
from app.utils.hash import verify_password

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

async def create_token(username: str):
    payload = {
        "username": username,
        "exp": datetime.utcnow() + timedelta(minutes=10)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return {"access_token": token, "token_type": "Bearer"}


async def sign_in(session: AsyncSession, form_data: OAuth2PasswordRequestForm):
    result = await session.execute(select(UserModel).filter(UserModel.username == form_data.username))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    return await create_token(user.username)

async def get_current_user(session: AsyncSession, token: HTTPAuthorizationCredentials):
    try:
        payload = jwt.decode(token.credentials, key=SECRET_KEY, algorithms=["HS256"])
        result = await session.execute(select(UserModel).filter(UserModel.username == payload.get("username")))
        user = result.scalars().first()
        if not user:
            raise {"status": "error", "detail": "User not found"}
        return {"status": "success", "detail": User(id=user.id, username=user.username, email=user.email)}
    except jwt.ExpiredSignatureError:
        return {"detail": "Token has expired"}
    except jwt.DecodeError:
        return {"detail": "Could not validate credentials"}
    except jwt.InvalidAlgorithmError:
        payload = VerifyToken(token.credentials).verify()
        result = await session.execute(select(UserModel).filter(UserModel.email == payload.get("user-email")))
        user = result.scalars().first()
        if not user:
            new_user = UserModel(username=None, email=payload.get("user-email"), password=None)
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return {"user": new_user}
        else:
            return {"status": "success", "detail": User(id=user.id, username=user.username, email=user.email)}