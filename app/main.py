from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy import select
from pydantic import ValidationError

from .db.db import async_session, AsyncSession, r
from .models.models import User as UserModel
from .schemas.schemas import User, SignUpRequestModel, SignInRequestModel, UserUpdateRequestModel, UsersListResponse, UserDetailResponse

from .utils.hash import get_password_hash

app = FastAPI()

@app.on_event("startup")
async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        yield session

@app.on_event("shutdown")
async def close_db_session():
    await r.close()



@app.get("/")
async def health_check():
    return {
        "status_code": 200,
        "detail": "ok",
        "result": "working"
    }

@app.get("/users", response_model=UsersListResponse)
async def get_users(session: AsyncSession = Depends(get_db_session)):
        result = await session.execute(select(UserModel))
        return {"users": result.scalars().all()}

@app.get("/users/{user_id}", response_model=UserDetailResponse)
async def get_user(user_id: int, session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(select(UserModel).filter(UserModel.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": user}

@app.post("/users/signup")
async def create_user(user: SignUpRequestModel, session: AsyncSession = Depends(get_db_session)):
    try:
        new_user = UserModel(username=user.username, email=user.email, password=get_password_hash(user.password))
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return {"user": new_user}
    except Exception:
        raise HTTPException(status_code=400)
    
@app.put("/users/{user_id}")
async def update_user(user_id: int, user_up: UserUpdateRequestModel, session: AsyncSession = Depends(get_db_session)):
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
        raise HTTPException(status_code=400)

@app.delete("/users/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_db_session)):
    try:
        result = await session.execute(select(UserModel).filter(UserModel.id == user_id))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        await session.delete(user)
        await session.commit()
        await session.close()
        return 'User was deleted'
    except Exception:
        raise HTTPException(status_code=400)