from app.db.db import AsyncSession, r
from sqlalchemy import select
from app.models.models import Result, Rating, Quiz, User, Company, Employees
from app.schemas.schemas import Score, RatingShema, PassedQuiz, ScoreCompany, LastEmployeesPassage
from fastapi import HTTPException

class AnaliticService():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_personal_rating(self, user_id: int):
        result = await self.session.execute(select(Rating).filter(Rating.user_id == user_id))
        rating = result.scalars().all()
        if not rating:
            return {'detail': 'You have not passed any quizzes yet'}
        user_rating = []
        for rate in rating:
            result = await self.session.execute(select(User).filter(User.id == user_id))
            user_email = result.scalars().first().email
            user_rating.append(RatingShema(user_email=user_email, company_id=rate.company_id, avg_scores=rate.scores, correct_answered=rate.correct_answered, total_answered=rate.total_questions))
        return {"ratings": user_rating}
        
    
    async def get_general_rating(self):
        result = await self.session.execute(select(Rating))
        rating = result.scalars().all()
        general_rating = []
        for rate in rating:
            result = await self.session.execute(select(User).filter(User.id == rate.user_id))
            user_email = result.scalars().first().email
            general_rating.append(RatingShema(user_email=user_email, company_id=rate.company_id, avg_scores=rate.scores, correct_answered=rate.correct_answered, total_answered=rate.total_questions))
        return {"ratings": general_rating}
    
    async def get_avg_scores_all_quizzes(self, user_id: int):
        result = await self.session.execute(select(Result).filter(Result.user_id == user_id))
        results = result.scalars().all()
        if not results:
            return {'detail': 'You have not passed any quizzes yet'}
        results = sorted(results, key=lambda x: x.time)
        scores = []
        for result in results:
            quiz = await self.session.execute(select(Quiz).filter(Quiz.id == result.quiz_id))
            quiz_name = quiz.scalars().first().name
            user_scores = result.correct_answered
            max_scores = result.count_questions
            accuracy = f'{(user_scores/max_scores):.1%}'
            scores.append(Score(quiz_name=quiz_name, score=user_scores, max_score=max_scores, accuracy=accuracy, time=str(result.time)))
        return {"scores": scores}
    
    async def get_passed_quizzes(self, user_id: int):
        result = await self.session.execute(select(Result).filter(Result.user_id == user_id))
        results = result.scalars().all()
        if not results:
            return {'detail': 'You have not passed any quizzes yet'}
        results = sorted(results, key=lambda x: x.time)
        passed_quizzes = []
        for result in results:
            quiz = await self.session.execute(select(Quiz).filter(Quiz.id == result.quiz_id))
            quiz_name = quiz.scalars().first().name
            passed_quizzes.append(PassedQuiz(quiz_name=quiz_name, time=str(result.time)))
        return {"passed_quizzes": passed_quizzes}
    
    async def get_scores_by_company(self, company_id: int, current_user: int):
        result = await self.session.execute(select(Company).filter(Company.id == company_id))
        company = result.scalars().first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        result = await self.session.execute(select(Employees).filter(Employees.company_id == company_id, Employees.user_id == current_user))
        user = result.scalars().first()
        if not user and company.owner_id != current_user:
            raise HTTPException(status_code=404, detail="You are not an employee of this company")
        if company.owner_id != current_user and user.is_admin == False:
            raise HTTPException(status_code=403, detail="You are not admin or owner of this company")
        result = await self.session.execute(select(Result).filter(Result.company_id == company_id))
        results = result.scalars().all()
        if not results:
            return {'detail': 'No one has taken any quizzes yet'}
        results = sorted(results, key=lambda x: x.time)
        company_results_avg = []
        for rate in results:
            quiz = await self.session.execute(select(Quiz).filter(Quiz.id == rate.quiz_id))
            quiz_name = quiz.scalars().first().name
            user = await self.session.execute(select(User).filter(User.id == rate.user_id))
            user_email = user.scalars().first().email
            user_scores = rate.correct_answered
            max_scores = rate.count_questions
            accuracy = f'{(user_scores/max_scores):.1%}'
            company_results_avg.append(ScoreCompany(user_email=user_email,quiz_name=quiz_name, accuracy=accuracy, time=str(rate.time)))
        return {"scores": company_results_avg}
    
    async def get_user_scores_by_company(self, company_id: int, current_user: int, user_id: int):
        result = await self.session.execute(select(Company).filter(Company.id == company_id))
        company = result.scalars().first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        result = await self.session.execute(select(Employees).filter(Employees.company_id == company_id, Employees.user_id == current_user))
        user = result.scalars().first()
        if not user and company.owner_id != current_user:
            raise HTTPException(status_code=404, detail="You are not an employee of this company")
        if company.owner_id != current_user and user.is_admin == False:
            raise HTTPException(status_code=403, detail="You are not admin or owner of this company")
        result = await self.session.execute(select(Result).filter(Result.company_id == company_id, Result.user_id == user_id))
        results = result.scalars().all()
        if not results:
            return {'detail': 'User has taken any quizzes yet'}
        user = await self.session.execute(select(User).filter(User.id == user_id))
        user_email = user.scalars().first().email
        results = sorted(results, key=lambda x: x.time)
        company_results_user_avg = []
        for rate in results:
            quiz = await self.session.execute(select(Quiz).filter(Quiz.id == rate.quiz_id))
            quiz_name = quiz.scalars().first().name
            user_scores = rate.correct_answered
            max_scores = rate.count_questions
            accuracy = f'{(user_scores/max_scores):.1%}'
            company_results_user_avg.append(ScoreCompany(user_email=user_email,quiz_name=quiz_name, accuracy=accuracy, time=str(rate.time)))
        return {"scores": company_results_user_avg}
    
    async def get_last_employees_passage(self, company_id: int, current_user: int):
        result = await self.session.execute(select(Company).filter(Company.id == company_id))
        company = result.scalars().first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        result = await self.session.execute(select(Employees).filter(Employees.company_id == company_id, Employees.user_id == current_user))
        user = result.scalars().first()
        if not user and company.owner_id != current_user:
            raise HTTPException(status_code=404, detail="You are not an employee of this company")
        if company.owner_id != current_user and user.is_admin == False:
            raise HTTPException(status_code=403, detail="You are not admin or owner of this company")
        result = await self.session.execute(select(Result).filter(Result.company_id == company_id))
        results = result.scalars().all()
        if not results:
            return {'detail': 'No one has taken any quizzes yet'}
        results = sorted(results, key=lambda x: x.time, reverse=True)
        last_employees_passage = []
        for res in results:
            if len(last_employees_passage) == 0 or res.user_id not in [item.user_id for item in last_employees_passage]:
                user = await self.session.execute(select(User).filter(User.id == res.user_id))
                user_email = user.scalars().first().email
                quiz = await self.session.execute(select(Quiz).filter(Quiz.id == res.quiz_id))
                quiz_name = quiz.scalars().first().name
                last_employees_passage.append(LastEmployeesPassage(user_id=res.user_id, user_email=user_email, quiz_name=quiz_name, time=str(res.time)))
        return {"last_employees_passage": last_employees_passage}
