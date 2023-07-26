from typing import List
from pydantic import BaseModel
from pydantic import EmailStr

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
