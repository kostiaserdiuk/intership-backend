from fastapi import APIRouter
from fastapi import Depends

from app.db.db import  AsyncSession, r
from app.utils.dependencies import get_db_session

from app.services.analitics import AnaliticService
from app.services.auth import get_current_user

from app.schemas.schemas import ScoresListResponse, RatingList, ScoresCompanyListResponse

router = APIRouter(
    prefix="/analitics",
    tags=["Analitics"],
)

@router.get("/rating/personal", response_model=RatingList)
async def get_rating(current_user: dict = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    return await AnaliticService(session).get_personal_rating(user_id=current_user.get("detail").id)

@router.get("/rating/all", response_model=RatingList)
async def get_rating_all(session: AsyncSession = Depends(get_db_session), current_user: dict = Depends(get_current_user)):
    return await AnaliticService(session).get_general_rating()

@router.get("/scores/avg", response_model=ScoresListResponse)
async def get_avg_scores(current_user: dict = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    return await AnaliticService(session).get_avg_scores_all_quizzes(user_id=current_user.get("detail").id)

@router.get("/quizzes/passed")
async def get_passed_quizzes(current_user: dict = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    return await AnaliticService(session).get_passed_quizzes(user_id=current_user.get("detail").id)

@router.get("/scores/avg/company/{company_id}", response_model=ScoresCompanyListResponse)
async def get_scores_by_company(company_id: int, session: AsyncSession = Depends(get_db_session), current_user: dict = Depends(get_current_user)):
    return await AnaliticService(session).get_scores_by_company(company_id=company_id, current_user=current_user.get("detail").id)

@router.get("/scores/avg/company/{company_id}/user/{user_id}", response_model=ScoresCompanyListResponse)
async def get_user_scores_by_company(company_id: int, user_id: int, session: AsyncSession = Depends(get_db_session), current_user: dict = Depends(get_current_user)):
    return await AnaliticService(session).get_user_scores_by_company(company_id=company_id, user_id=user_id, current_user=current_user.get("detail").id)

@router.get("/last/employees/passage/company/{company_id}")
async def get_last_employees_passage(company_id: int, session: AsyncSession = Depends(get_db_session), current_user: dict = Depends(get_current_user)):
    return await AnaliticService(session).get_last_employees_passage(company_id=company_id, current_user=current_user.get("detail").id)