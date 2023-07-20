from app.db.db import AsyncSession
from app.models.models import User as UserModel
from app.schemas.schemas import SignUpRequestModel,  UserUpdateRequestModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.utils.hash import get_password_hash

async def users(session: AsyncSession):
    result = await session.execute(select(UserModel))
    return {"users": result.scalars().all()}

async def user(user_id: int, session: AsyncSession):
    result = await session.execute(select(UserModel).filter(UserModel.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": user}

async def create_user(user: SignUpRequestModel, session: AsyncSession):
    try:
        new_user = UserModel(username=user.username, email=user.email, password=get_password_hash(user.password))
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return {"user": new_user}
    except IntegrityError:
        raise HTTPException(status_code=409, detail="User already exists")
    
async def update_user(user_id: int, user_up: UserUpdateRequestModel, session: AsyncSession):
    try:
        result = await session.execute(select(UserModel).filter(UserModel.id == user_id))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.username = user_up.username
        user.email = user_up.email
        user.password = get_password_hash(user_up.password)
        await session.commit()
        await session.refresh(user)
        return {"user": user}
    except Exception:
        raise HTTPException(status_code=400, detail="Bad request")
    
async def delete_user(user_id: int, session: AsyncSession):
        result = await session.execute(select(UserModel).filter(UserModel.id == user_id))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        await session.delete(user)
        await session.commit()
        await session.close()
        return {"detail" : "User was deleted"}