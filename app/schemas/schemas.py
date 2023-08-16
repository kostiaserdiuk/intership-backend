from typing import List
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import field_validator

class User(BaseModel):
    id: int
    username: str | None
    email: str
    # class Config:
    #     orm_mode = True
    #     allow_population_by_field_name = True
    #     arbitrary_types_allowed = True


class SignInRequestModel(BaseModel):
    username: str
    password: str

class SignUpRequestModel(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserUpdateRequestModel(BaseModel):
    username: str
    email: EmailStr
    password: str

class UsersListResponse(BaseModel):
    users: List[User]

class UserDetailResponse(BaseModel):
    user: User

class UserDelatedResponse(BaseModel):
    detail: str
    user: User

class Token(BaseModel):
    access_token: str
    token_type: str

class AuthResponse(BaseModel):
    status: str
    detail: User | str

class UserPersonalEdit(BaseModel):
    username: str
    password: str

class Company(BaseModel):
    id: int
    name: str
    description: str
    owner_id: int

class CompanyCreateRequestModel(BaseModel):
    name: str
    description: str

class CompanyCreateResponseModel(BaseModel):
    company: Company

class CompanyUpdateResponseModel(BaseModel):
    name: str
    description: str

class CompanyListResponse(BaseModel):
    companies: List[Company]

class Question(BaseModel):
    question: str
    answers: List[str]
    correct_answer: str

class Quiz(BaseModel):
    name: str
    description: str
    frequency: int
    questions: List[Question]

    @field_validator('questions')
    def check_questions(cls, v):
        if len(v) < 2:
            raise ValueError('Questions must be at least 2')
        for question in v:
            if len(question.answers) < 2:
                raise ValueError('Answers must be at least 2')
        return v

class QuizzesListResponse(BaseModel):
    quizzes: List[Quiz]

class QuizPassing(BaseModel):
    answers: List[str]

    @field_validator('answers')
    def check_questions(cls, v):
        if len(v) < 2:
            raise ValueError('Answers must be at least 2')
        return v

class Score(BaseModel):
    quiz_name: str
    score: int
    max_score: int
    accuracy: str
    time: str

class ScoresListResponse(BaseModel):
    scores: List[Score]

class RatingShema(BaseModel):
    user_email: str
    company_id: int
    avg_scores: float
    correct_answered: int
    total_answered: int

class RatingList(BaseModel):
    ratings: List[RatingShema]

class PassedQuiz(BaseModel):
    quiz_name: str
    time: str

class ScoreCompany(BaseModel):
    user_email: str
    quiz_name: str
    accuracy: str
    time: str

class ScoresCompanyListResponse(BaseModel):
    scores: List[ScoreCompany]

class LastEmployeesPassage(BaseModel):
    user_id: int
    user_email: str
    quiz_name: str
    time: str

class LastEmployeesPassageListResponse(BaseModel):
    last_employees_passage: List[LastEmployeesPassage]