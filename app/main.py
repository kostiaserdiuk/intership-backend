from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException

from .db.db import async_session, AsyncSession, r
from .schemas.schemas import SignUpRequestModel, UserUpdateRequestModel, UsersListResponse, UserDetailResponse

from .services.crud import users, user, create_user, update_user, delete_user

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
        return await users(session)

@app.get("/users/{user_id}", response_model=UserDetailResponse)
async def get_user(user_id: int, session: AsyncSession = Depends(get_db_session)):
    return await user(user_id, session)

@app.post("/users/signup", status_code=201)
async def sign_up(user: SignUpRequestModel, session: AsyncSession = Depends(get_db_session)):
    return await create_user(user, session)
    
@app.put("/users/{user_id}", response_model=UserDetailResponse)
async def update(user_id: int, user_up: UserUpdateRequestModel, session: AsyncSession = Depends(get_db_session)):
    return await update_user(user_id, user_up, session)

@app.delete("/users/{user_id}")
async def remove(user_id: int, session: AsyncSession = Depends(get_db_session)):
    return await delete_user(user_id, session)