from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import StreamingResponse
from app.utils.dependencies import get_db_session
from app.db.db import  AsyncSession, r
from app.services.auth import get_current_user
from app.services.quiz import QuizService, QuizPassage
from app.schemas.schemas import Quiz, QuizzesListResponse, QuizPassing
from enum import Enum

router = APIRouter(
    prefix="/quizzes",
    tags=["Quizzes"],
)

class ExportModel(str, Enum):
    json = "json"
    csv = "csv"

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
async def get_quizzes(company_id: int, current_user: dict = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    return await QuizService(session).get_quizzes(company_id=company_id, current_user=current_user.get("detail").id)

@router.post("/passage/{company_id}/{quiz_name}")
async def quiz_passage(quiz_passing: QuizPassing, 
                        company_id: int,
                        quiz_name: str, 
                        current_user: dict = Depends(get_current_user), 
                        session: AsyncSession = Depends(get_db_session)):
    return await QuizPassage(session).quiz_passing(company_id=company_id, quiz_name=quiz_name, current_user=current_user.get("detail").id, quiz_passing=quiz_passing)

@router.get("/company/{company_id}/statistic")
async def get_statistics(company_id: int, current_user: dict = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    return await QuizService(session).get_statistic_by_company(company_id=company_id, current_user=current_user.get("detail").id)

@router.get("/general/statistic")
async def get_general_statistics(current_user: dict = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    return await QuizService(session).get_general_statistic(current_user=current_user.get("detail").id)

@router.get("/user/export/{export_model}")
async def export_user_results(export_model: ExportModel, current_user: dict = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    if export_model == ExportModel.json or export_model == ExportModel.csv:
        return await QuizService(session).user_export_results(current_user=current_user.get("detail").id, export_model=export_model)
    return {"status": "error", "detail": "Wrong export model"}

@router.get("/company/{company_id}/export/{export_model}")
async def export_company_results(export_model: ExportModel, company_id: int, current_user: dict = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    if export_model == ExportModel.json or export_model == ExportModel.csv:
        return await QuizService(session).admin_export_results(company_id=company_id, current_user=current_user.get("detail").id, export_model=export_model)
    # return await QuizService(session).admin_export_results(company_id=company_id, current_user=current_user.get("detail").id)
    return {"status": "error", "detail": "Wrong export model"}