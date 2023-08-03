from fastapi import APIRouter
from fastapi import Depends
from app.utils.dependencies import get_db_session
from app.db.db import  AsyncSession, r
from app.services.auth import get_current_user
from app.services.quiz import QuizService
from app.schemas.schemas import Quiz, QuizzesListResponse

router = APIRouter(
    prefix="/quizzes",
    tags=["Quizzes"],
)

@router.post("/company/{company_id}/create")
async def create_quiz(quiz: Quiz, company_id: int, current_user: dict = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    return await QuizService(session).create_quiz(quiz=quiz, company_id=company_id, current_user=current_user.get("detail").id)

@router.put("/{quiz_name}/update")
async def update_quiz(quiz: Quiz, quiz_name: str, current_user: dict = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    return await QuizService(session).update_quiz(quiz=quiz, quiz_name=quiz_name, current_user=current_user.get("detail").id)

@router.delete("/{quiz_name}/delete")
async def delete_quiz(quiz_name: str, current_user: dict = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    return await QuizService(session).delete_quiz(quiz_name=quiz_name, current_user=current_user.get("detail").id)

@router.get("/company/{company_id}/list", response_model=QuizzesListResponse)
async def list_quizzes(company_id: int, current_user: dict = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    return await QuizService(session).list_quizzes(company_id=company_id, current_user=current_user.get("detail").id)