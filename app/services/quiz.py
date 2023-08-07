from app.db.db import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from app.models.models import Company, Employees
from app.models.models import Quiz as QuizModel
from app.models.models import Result, Rating
from app.schemas.schemas import Quiz, QuizPassing
from datetime import datetime


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

    async def get_quizzes(self, company_id: int, current_user: int):
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
        result = await self.session.execute(select(QuizModel).filter(QuizModel.company_id == company_id))
        quizzes = result.scalars().all()
        quizzes = [Quiz(name=quiz.name, description=quiz.description, frequency=quiz.frequency, questions=quiz.questions) for quiz in quizzes]
        return {"quizzes": quizzes}
    
    async def get_statistic_by_company(self, current_user: int, company_id: int):
        result = await self.session.execute(select(Rating).filter(Rating.user_id == current_user, Rating.company_id == company_id))
        ratings = result.scalars().first()
        if not ratings:
            raise HTTPException(status_code=404, detail="You have not passed any quizzes in this company")
        scores = ratings.scores
        return {"scores": scores}
    
    async def get_general_statistic(self, current_user: int):
        result = await self.session.execute(select(Rating).filter(Rating.user_id == current_user))
        ratings = result.scalars().all()
        if not ratings:
            raise HTTPException(status_code=404, detail="You have not passed any quizzes")
        all_correct_answers = sum([row.correct_answered for row in ratings])
        all_questions = sum([row.total_questions for row in ratings])
        general_score = float(f"{all_correct_answers/all_questions:.2f}")
        return {"general_score": general_score}
        

    
class QuizPassage:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def quiz_passing (self, quiz_passing: QuizPassing, quiz_name: str, company_id: int, current_user: int):
        result = await self.session.execute(select(Company).filter(Company.id == company_id))
        company = result.scalars().first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        result = await self.session.execute(select(Employees).filter(Employees.company_id == company_id, Employees.user_id == current_user))
        user = result.scalars().first()
        if not user and company.owner_id != current_user:
            raise HTTPException(status_code=404, detail="You are not an employee of this company")
        result = await self.session.execute(select(QuizModel).filter(QuizModel.name == quiz_name, QuizModel.company_id == company_id))
        quiz_model = result.scalars().first()
        if not quiz_model:
            raise HTTPException(status_code=404, detail="Quiz not found")
        user_answers = quiz_passing.answers
        questions = quiz_model.questions
        correct_answers = [question.get("correct_answer") for question  in questions]
        if len(user_answers) != len(correct_answers):
            raise HTTPException(status_code=400, detail="Wrong number of answers")
        points = sum([1 for user_answer, correct_answer in zip(user_answers, correct_answers) if user_answer == correct_answer])
        result = await self.session.execute(select(Result).filter(Result.user_id == current_user, Result.quiz_id == quiz_model.id, Result.company_id == company_id))
        result_model = result.scalars().first()
        if result_model:
            raise HTTPException(status_code=409, detail="You have already passed this quiz")
        now = datetime.utcnow()
        result_model = Result(user_id=current_user, quiz_id=quiz_model.id, company_id=company_id, correct_answered=points, count_questions=len(correct_answers), time=now)
        self.session.add(result_model)
        await self.session.commit()
        await self.session.refresh(result_model)
        
        rating = await self.session.execute(select(Rating).filter(Rating.user_id == current_user, Rating.company_id == company_id))
        rating_model = rating.scalars().first()
        if not rating_model:
            scores = float(f"{(points/len(correct_answers)):.2f}")
            rating_model = Rating(user_id=current_user, company_id=company_id, scores=scores, correct_answered=points, total_questions=len(correct_answers), time=now)
            self.session.add(rating_model)
            await self.session.commit()
            await self.session.refresh(rating_model)
        else:
            rating_model.scores = float(f"{((rating_model.correct_answered + points)/(rating_model.total_questions + len(correct_answers))):.2f}")
            rating_model.correct_answered += points
            rating_model.total_questions += len(correct_answers)
            rating_model.time = now
            await self.session.commit()
            await self.session.refresh(rating_model)
        return {result_model, rating_model}