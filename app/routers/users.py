from fastapi import APIRouter
from fastapi import Depends
from app.schemas.schemas import SignUpRequestModel, UserUpdateRequestModel, UsersListResponse, UserDetailResponse

from app.utils.dependencies import get_db_session, close_db_session
from app.db.db import  AsyncSession, r
from app.services.crud import users, user, create_user, update_user, delete_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get("/", response_model=UsersListResponse)
async def get_users(session: AsyncSession = Depends(get_db_session)):
        return await users(session)

@router.get("/{user_id}", response_model=UserDetailResponse)
async def get_user(user_id: int, session: AsyncSession = Depends(get_db_session)):
    return await user(user_id, session)

@router.post("/signup", status_code=201)
async def sign_up(user: SignUpRequestModel, session: AsyncSession = Depends(get_db_session)):
    return await create_user(user, session)
    
@router.put("/{user_id}", response_model=UserDetailResponse)
async def update(user_id: int, user_up: UserUpdateRequestModel, session: AsyncSession = Depends(get_db_session)):
    return await update_user(user_id, user_up, session)

@router.delete("/{user_id}")
async def remove(user_id: int, session: AsyncSession = Depends(get_db_session)):
    return await delete_user(user_id, session)