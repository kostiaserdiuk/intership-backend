from fastapi import APIRouter
from fastapi import Depends
from app.schemas.schemas import SignUpRequestModel, UserUpdateRequestModel, UsersListResponse, UserDetailResponse, UserDelatedResponse

from app.utils.dependencies import get_db_session, close_db_session
from app.db.db import  AsyncSession, r
from app.services.crud import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get("/", response_model=UsersListResponse)
async def get_users(session: AsyncSession = Depends(get_db_session)):
        return await UserService(session).users()

@router.get("/{user_id}", response_model=UserDetailResponse)
async def get_user(user_id: int, session: AsyncSession = Depends(get_db_session)):
    return await UserService(session).user(user_id=user_id)

@router.post("/signup", status_code=201, response_model=UserDetailResponse)
async def sign_up(user: SignUpRequestModel, session: AsyncSession = Depends(get_db_session)):
    return await UserService(session).create_user(user=user)
    
@router.put("/{user_id}", response_model=UserDetailResponse)
async def update(user_id: int, user_up: UserUpdateRequestModel, session: AsyncSession = Depends(get_db_session)):
    return await UserService(session).update_user(user_id=user_id, user_up=user_up)

@router.delete("/{user_id}", response_model=UserDelatedResponse)
async def remove(user_id: int, session: AsyncSession = Depends(get_db_session)):
    return await UserService(session).delete_user(user_id)