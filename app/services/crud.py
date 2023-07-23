from app.db.db import AsyncSession
from app.models.models import User as UserModel
from app.schemas.schemas import SignUpRequestModel,  UserUpdateRequestModel, UserDetailResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.utils.hash import get_password_hash

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def users(self) -> dict:
        result = await self.session.execute(select(UserModel))
        return {"users": result.scalars().all()}
    
    async def user(self, user_id: int) -> dict:
        result = await self.session.execute(select(UserModel).filter(UserModel.id == user_id))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"user": user}
    
    async def create_user(self, user: SignUpRequestModel) -> dict:
        try:
            new_user = UserModel(username=user.username, email=user.email, password=get_password_hash(user.password))
            self.session.add(new_user)
            await self.session.commit()
            await self.session.refresh(new_user)
            return {"user": new_user}
        except IntegrityError:
            raise HTTPException(status_code=409, detail="User already exists")
    
    async def update_user(self, user_id: int, user_up: UserUpdateRequestModel) -> dict:
            result = await self.session.execute(select(UserModel).filter(UserModel.id == user_id))
            user = result.scalars().first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            user.username = user_up.username
            user.email = user_up.email
            user.password = get_password_hash(user_up.password)
            await self.session.commit()
            await self.session.refresh(user)
            return {"user": user}
    
    async def delete_user(self, user_id: int) -> dict:
            result = await self.session.execute(select(UserModel).filter(UserModel.id == user_id))
            user = result.scalars().first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            await self.session.delete(user)
            await self.session.commit()
            await self.session.close()
            return {"detail" : "User was deleted", "user" : user}
