from app.db.db import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from app.models.models import Company, Employees
from app.models.models import Quiz as QuizModel
from app.schemas.schemas import Quiz


class QuizService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_quiz(self, quiz: Quiz, company_id: int, current_user: int):
        result = await self.session.execute(select(Company).filter(Company.id == company_id))
        company = result.scalars().first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        result = await self.session.execute(select(Employees).filter(Employees.company_id == company_id, Employees.user_id == current_user))
        user = result.scalars().first()
        if not user and company.owner_id != current_user:
            raise HTTPException(status_code=404, detail="You are not an employee of this company")
        if company.owner_id != current_user and user.is_admin == False:
            raise HTTPException(status_code=403, detail="You are not allowed to create quizzes")
        try:
            new_quiz = QuizModel(name=quiz.name, description=quiz.description, company_id=company_id, frequency=quiz.frequency, questions=jsonable_encoder(quiz.questions))
            self.session.add(new_quiz)
            await self.session.commit()
            await self.session.refresh(new_quiz)
            return {"quiz": new_quiz}
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Quiz already exists")
        
    async def update_quiz(self, quiz: Quiz, quiz_name: str, current_user: int):
        result = await self.session.execute(select(QuizModel).filter(QuizModel.name == quiz_name))
        quiz_model = result.scalars().first()
        if not quiz_model:
            raise HTTPException(status_code=404, detail="Quiz not found")
        company_id = quiz_model.company_id
        result = await self.session.execute(select(Company).filter(Company.id == company_id))
        company = result.scalars().first()
        result = await self.session.execute(select(Employees).filter(Employees.company_id == company_id, Employees.user_id == current_user))
        user = result.scalars().first()
        if not user and company.owner_id != current_user:
            raise HTTPException(status_code=404, detail="You are not an employee of this company")
        if company.owner_id != current_user and user.is_admin == False:
            raise HTTPException(status_code=403, detail="You are not allowed to create quizzes")
        try:
            result = await self.session.execute(select(QuizModel).filter(QuizModel.name == quiz_name))
            quiz_model = result.scalars().first()
            quiz_model.name = quiz.name
            quiz_model.description = quiz.description
            quiz_model.frequency = quiz.frequency
            quiz_model.questions = jsonable_encoder(quiz.questions)
            await self.session.commit()
            await self.session.refresh(quiz_model)
            return {"quiz": quiz_model}
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Quiz name already exists")
        
    async def delete_quiz(self, quiz_name: str, current_user: int):
        result = await self.session.execute(select(QuizModel).filter(QuizModel.name == quiz_name))
        quiz_model = result.scalars().first()
        if not quiz_model:
            raise HTTPException(status_code=404, detail="Quiz not found")
        company_id = quiz_model.company_id
        result = await self.session.execute(select(Company).filter(Company.id == company_id))
        company = result.scalars().first()
        result = await self.session.execute(select(Employees).filter(Employees.company_id == company_id, Employees.user_id == current_user))
        user = result.scalars().first()
        if not user and company.owner_id != current_user:
            raise HTTPException(status_code=404, detail="You are not an employee of this company")
        if company.owner_id != current_user and user.is_admin == False:
            raise HTTPException(status_code=403, detail="You are not allowed to create quizzes")
        result = await self.session.execute(select(QuizModel).filter(QuizModel.name == quiz_name))
        quiz_model = result.scalars().first()
        await self.session.delete(quiz_model)
        await self.session.commit()
        await self.session.close()
        return {"status": "Quiz deleted successfully"}

    async def list_quizzes(self, company_id: int, current_user: int):
        result = await self.session.execute(select(Company).filter(Company.id == company_id))
        company = result.scalars().first()
        result = await self.session.execute(select(Employees).filter(Employees.company_id == company_id, Employees.user_id == current_user))
        user = result.scalars().first()
        if not user and company.owner_id != current_user:
            raise HTTPException(status_code=404, detail="You are not an employee of this company")
        if company.owner_id != current_user and user.is_admin == False:
            raise HTTPException(status_code=403, detail="You are not allowed to create quizzes")
        result = await self.session.execute(select(QuizModel).filter(QuizModel.company_id == company_id))
        quizzes = result.scalars().all()
        quizzes = [Quiz(name=quiz.name, description=quiz.description, frequency=quiz.frequency, questions=quiz.questions) for quiz in quizzes]
        return {"quizzes": quizzes}
    
