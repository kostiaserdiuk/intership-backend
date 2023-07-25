from fastapi import APIRouter
from fastapi import Depends
from app.schemas.schemas import CompanyCreateRequestModel, CompanyListResponse, Company, CompanyCreateResponseModel, CompanyUpdateResponseModel
from app.utils.dependencies import get_db_session
from app.db.db import  AsyncSession, r
from app.services.crud import CompanyService
from app.services.auth import get_current_user

router = APIRouter(
    prefix="/companies",
    tags=["Companies"],
)

@router.post("/create", status_code=201, response_model=CompanyCreateResponseModel)
async def create_company(company: CompanyCreateRequestModel, session: AsyncSession = Depends(get_db_session), current_user: dict = Depends(get_current_user)):
    return await CompanyService(session).create_company(company=company, owner_id=current_user.get('detail').id)

@router.get("/get/{company_id}", response_model=Company)
async def get_company(company_id: int, session: AsyncSession = Depends(get_db_session)):
    return await CompanyService(session).get_company(company_id=company_id)

@router.put("/update/{company_name}", response_model=CompanyUpdateResponseModel)
async def update_company(company_name: str, company_up: CompanyCreateRequestModel, session: AsyncSession = Depends(get_db_session), current_user: dict = Depends(get_current_user)):
    return await CompanyService(session).update_company(company_name=company_name, company_up=company_up, user_id=current_user.get('detail').id)

@router.delete("/delete/{company_name}")
async def remove_company(company_name: str, session: AsyncSession = Depends(get_db_session), current_user: dict = Depends(get_current_user)):
    return await CompanyService(session).delete_company(company_name=company_name, user_id=current_user.get('detail').id)

@router.get("/list", response_model=CompanyListResponse)
async def get_companies(session: AsyncSession = Depends(get_db_session)):
    return await CompanyService(session).companies()