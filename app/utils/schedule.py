
from app.utils.dependencies import get_db_session
from app.db.db import async_session
from app.models.models import Notification, Result, Quiz, Company
from fastapi import Depends

from sqlalchemy import select

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from loguru import logger


class SchedulerService:
    def __init__(self):
        scheduler = AsyncIOScheduler()
        scheduler.add_job(self.scheduler_notification, 'cron', hour='0', minute='0', day='*')
        scheduler.start()
        logger.info('Scheduler started')

    async def scheduler_notification(self):
        async with async_session() as self.session:
            result = await self.session.execute(select(Result))
            results = result.scalars().all()
            if not results:
                return
            for result in results:
                user_id, quiz_id, user_time = result.user_id, result.quiz_id, result.time
                quiz = await self.session.execute(select(Quiz).filter(Quiz.id == quiz_id))
                quiz = quiz.scalars().first()
                if not quiz:
                    continue
                company = await self.session.execute(select(Company).filter(Company.id == quiz.company_id))
                company_name = company.scalars().first().name
                if not company_name:
                    company_name = 'unknown'
                quiz_time = quiz.time_to_pass
                if user_time > quiz_time:
                    notification = Notification(user_id=user_id, message=f'You took the quiz {quiz.name} late in {company_name} company', time=datetime.utcnow())
                    result = await self.session.execute(select(Notification).filter(Notification.user_id == user_id, Notification.message == notification.message))
                    result = result.scalars().first()
                    if result:
                        continue
                    self.session.add(notification)
                    await self.session.commit()
                    await self.session.refresh(notification)
