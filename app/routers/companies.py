from fastapi import APIRouter
from fastapi import Depends
from app.schemas.schemas import (
    CompanyCreateRequestModel,
    CompanyListResponse,
    Company,
    CompanyCreateResponseModel,
    CompanyUpdateResponseModel,
)
from app.utils.dependencies import get_db_session
from app.db.db import AsyncSession, r
from app.services.crud import CompanyService
from app.services.company_action import CompanyActions, UserActions
from app.services.auth import get_current_user

router = APIRouter(
    prefix="/companies",
    tags=["Companies"],
)


@router.post("/create", status_code=201, response_model=CompanyCreateResponseModel)
async def create_company(
    company: CompanyCreateRequestModel,
    session: AsyncSession = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    return await CompanyService(session).create_company(
        company=company, owner_id=current_user.get("detail").id
    )


@router.put("/update/{company_name}", response_model=CompanyUpdateResponseModel)
async def update_company(
    company_name: str,
    company_up: CompanyCreateRequestModel,
    session: AsyncSession = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    return await CompanyService(session).update_company(
        company_name=company_name,
        company_up=company_up,
        user_id=current_user.get("detail").id,
    )


@router.delete("/delete/{company_name}")
async def remove_company(
    company_name: str,
    session: AsyncSession = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    return await CompanyService(session).delete_company(
        company_name=company_name, user_id=current_user.get("detail").id
    )


@router.get("/list", response_model=CompanyListResponse)
async def get_companies(session: AsyncSession = Depends(get_db_session)):
    return await CompanyService(session).companies()


@router.post("/invite/{company_id}/{user_id}")
async def invite_user(
    company_id: int,
    user_id: int,
    session: AsyncSession = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    return await CompanyActions(session).invite(
        company_id=company_id,
        user_id=user_id,
        current_user=current_user.get("detail").id,
    )


@router.post("/invite/reject/{company_id}/{user_id}")
async def reject_invite(
    company_id: int,
    user_id: int,
    session: AsyncSession = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    return await CompanyActions(session).reject_invite(
        company_id=company_id,
        user_id=user_id,
        current_user=current_user.get("detail").id,
    )


@router.post("/accept/invite/{company_id}")
async def accept_invite(
    company_id: int,
    session: AsyncSession = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    return await UserActions(session).accept_invite(
        company_id=company_id, user_id=current_user.get("detail").id
    )


@router.post("/decline/invite/{company_id}")
async def decline_invite(
    company_id: int,
    session: AsyncSession = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    return await UserActions(session).decline_invite(
        company_id=company_id, user_id=current_user.get("detail").id
    )


@router.post("/join/company/{company_id}")
async def join_company(
    company_id: int,
    session: AsyncSession = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    return await UserActions(session).request_to_company(
        company_id=company_id, user_id=current_user.get("detail").id
    )


@router.post("/join/cancel/{company_id}")
async def cancel_join(
    company_id: int,
    session: AsyncSession = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    return await UserActions(session).cancel_request(
        company_id=company_id, user_id=current_user.get("detail").id
    )


@router.post("/join/accept/{company_id}/{user_id}")
async def accept_join(
    company_id: int,
    user_id: int,
    session: AsyncSession = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    return await CompanyActions(session).accept_request(
        company_id=company_id,
        user_id=user_id,
        current_user=current_user.get("detail").id,
    )


@router.post("/join/decline/{company_id}/{user_id}")
async def decline_join(
    company_id: int,
    user_id: int,
    session: AsyncSession = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    return await CompanyActions(session).decline_request(
        company_id=company_id,
        user_id=user_id,
        current_user=current_user.get("detail").id,
    )


@router.post("/kick/{company_id}/{user_id}")
async def kick_user(
    company_id: int,
    user_id: int,
    session: AsyncSession = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    return await CompanyActions(session).kick(
        company_id=company_id,
        user_id=user_id,
        current_user=current_user.get("detail").id,
    )


@router.post("/leave/{company_id}")
async def leave_company(
    company_id: int,
    session: AsyncSession = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    return await UserActions(session).leave_company(
        company_id=company_id, user_id=current_user.get("detail").id
    )


@router.get("/get/invites")
async def get_invites(
    session: AsyncSession = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    return await UserActions(session).invites(user_id=current_user.get("detail").id)


@router.get("/get/requests")
async def get_requests(
    session: AsyncSession = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    return await UserActions(session).requests(user_id=current_user.get("detail").id)


@router.get("/get/members/{company_id}")
async def get_members(
    company_id: int,
    session: AsyncSession = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    return await CompanyActions(session).employees(
        company_id=company_id, current_user=current_user.get("detail").id
    )


@router.get("/get/company/requests/{company_id}")
async def get_company_requests(
    company_id: int,
    session: AsyncSession = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    return await CompanyActions(session).requests(
        company_id=company_id, current_user=current_user.get("detail").id
    )


@router.get("/get/company/invites/{company_id}")
async def get_company_invites(
    company_id: int,
    session: AsyncSession = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    return await CompanyActions(session).invited(
        company_id=company_id, current_user=current_user.get("detail").id
    )


@router.post("/assign/admin/{company_id}/{user_id}")
async def assign_admin(
    company_id: int,
    user_id: int,
    session: AsyncSession = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    return await CompanyActions(session).assign_admin(
        company_id=company_id,
        user_id=user_id,
        current_user=current_user.get("detail").id,
    )


@router.post("/unassign/admin/{company_id}/{user_id}")
async def unassign_admin(
    company_id: int,
    user_id: int,
    session: AsyncSession = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    return await CompanyActions(session).unassign_admin(
        company_id=company_id,
        user_id=user_id,
        current_user=current_user.get("detail").id,
    )


@router.get("/company/admins/{company_id}")
async def get_admins(
    company_id: int,
    session: AsyncSession = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    return await CompanyActions(session).get_admins(
        company_id=company_id, current_user=current_user.get("detail").id
    )


@router.get("/get/{company_id}", response_model=Company)
async def get_company(company_id: int, session: AsyncSession = Depends(get_db_session)):
    return await CompanyService(session).get_company(company_id=company_id)
