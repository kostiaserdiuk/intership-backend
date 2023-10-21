from app.db.db import AsyncSession, r
from sqlalchemy import select
from app.models.models import Employees, Notification, Company
from app.schemas.schemas import NotificationShema
from datetime import datetime
from fastapi import HTTPException


class NotificationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def quiz_notification(self, quiz_name: str, company_id: int):
        result = await self.session.execute(
            select(Employees).filter(Employees.company_id == company_id)
        )
        employees = result.scalars().all()
        if not employees:
            return
        result = await self.session.execute(
            select(Company).filter(Company.id == company_id)
        )
        company_name = result.scalars().first().name
        now = datetime.utcnow()
        for employee in employees:
            new_notification = Notification(
                user_id=employee.user_id,
                message=f"You have new quiz {quiz_name} in {company_name} company, please pass it",
                time=now,
            )
            self.session.add(new_notification)
            await self.session.commit()
            await self.session.refresh(new_notification)

    async def check_notifications(self, user_id: int):
        result = await self.session.execute(
            select(Notification).filter(
                Notification.user_id == user_id, Notification.is_read == False
            )
        )
        notifications = result.scalars().all()
        if not notifications:
            raise HTTPException(status_code=200, detail="You have no notifications")
        # notifications = sorted(notifications, key=lambda x: x.time)
        notifications_response = [
            NotificationShema(id=notification.id, message=notification.message)
            for notification in notifications
        ]
        return {"notifications": notifications_response}

    async def read_notification(self, notification_id: int, user_id: int):
        notification = await self.session.execute(
            select(Notification).filter(
                Notification.id == notification_id, Notification.user_id == user_id
            )
        )
        notification = notification.scalars().first()
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        notification.is_read = True
        await self.session.commit()
        return {"detail": "Notification was read"}
