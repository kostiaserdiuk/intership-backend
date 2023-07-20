from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials

from app.db.db import  AsyncSession, r
from app.utils.dependencies import get_db_session, close_db_session

from app.schemas.schemas import SignInRequestModel, Token

from app.services.auth import sign_in, get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

security = HTTPBearer()

@router.post("/login", response_model=Token)
async def login(session: AsyncSession=Depends(get_db_session), form_data: OAuth2PasswordRequestForm=Depends(SignInRequestModel)):
    return await sign_in(session, form_data)

@router.get("/me")
async def me(session: AsyncSession=Depends(get_db_session), token: HTTPAuthorizationCredentials = Depends(security)):
    return await get_current_user(session, token)
