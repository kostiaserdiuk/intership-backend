from fastapi import APIRouter
from fastapi import Depends
from app.schemas.schemas import (
    SignUpRequestModel,
    UserUpdateRequestModel,
    UsersListResponse,
    UserDetailResponse,
    UserDelatedResponse,
    UserPersonalEdit,
    AuthResponse,
)

from app.utils.dependencies import get_db_session, close_db_session
from app.db.db import AsyncSession, r
from app.services.crud import UserService
from app.services.auth import get_current_user

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
async def sign_up(
    user: SignUpRequestModel, session: AsyncSession = Depends(get_db_session)
):
    return await UserService(session).create_user(user=user)


@router.put("/update", response_model=UserDetailResponse)
async def update(
    user_up: UserPersonalEdit,
    session: AsyncSession = Depends(get_db_session),
    current_user: AuthResponse = Depends(get_current_user),
):
    return await UserService(session).update_user(
        user_id=current_user.get("detail").id, user_up=user_up
    )


@router.delete("/delete", response_model=UserDelatedResponse)
async def remove(
    session: AsyncSession = Depends(get_db_session),
    current_user: AuthResponse = Depends(get_current_user),
):
    return await UserService(session).delete_user(user_id=current_user.get("detail").id)
