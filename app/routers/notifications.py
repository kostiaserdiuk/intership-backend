from fastapi import APIRouter
from fastapi import Depends

from app.utils.dependencies import get_db_session
from app.db.db import AsyncSession, r
from app.services.auth import get_current_user

from app.schemas.schemas import NotificationListResponse

from app.services.notifications import NotificationService

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@router.get("/check", response_model=NotificationListResponse)
async def check_notifications(
    session: AsyncSession = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    return await NotificationService(session).check_notifications(
        user_id=current_user.get("detail").id
    )


@router.get("/read/{notification_id}")
async def read_notification(
    notification_id: int,
    session: AsyncSession = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    return await NotificationService(session).read_notification(
        notification_id=notification_id, user_id=current_user.get("detail").id
    )
