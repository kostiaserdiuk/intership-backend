from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.db.db import AsyncSession, r
from app.utils.dependencies import get_db_session

from app.schemas.schemas import SignInRequestModel, Token, AuthResponse

from app.services.auth import AuthService, get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/login", response_model=Token)
async def login(
    session: AsyncSession = Depends(get_db_session),
    form_data: OAuth2PasswordRequestForm = Depends(SignInRequestModel),
):
    return await AuthService(session).sign_in(form_data)


@router.get("/me", response_model=AuthResponse)
async def me(user: AuthResponse = Depends(get_current_user)):
    return user
