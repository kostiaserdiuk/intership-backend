from typing import List
from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    email: str

class SignInRequestModel(BaseModel):
    username: str
    password: str

class SignUpRequestModel(BaseModel):
    username: str
    email: str
    password: str

class UserUpdateRequestModel(BaseModel):
    username: str
    email: str
    password: str

class UsersListResponse(BaseModel):
    users: List[User]

class UserDetailResponse(BaseModel):
    user: User