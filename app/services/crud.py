from app.db.db import AsyncSession
from app.models.models import User as UserModel
from app.models.models import Company as CompanyModel
from app.models.models import CompanyAction as CompanyActionModel
from app.schemas.schemas import SignUpRequestModel, UserPersonalEdit, CompanyCreateRequestModel, Company, CompanyListResponse
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
    
    async def update_user(self, user_id: int, user_up: UserPersonalEdit) -> dict:
            result = await self.session.execute(select(UserModel).filter(UserModel.id == user_id))
            user = result.scalars().first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            user.username = user_up.username
            user.email = user.email
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

class CompanyService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_company(self, company: CompanyCreateRequestModel, owner_id: int) -> dict:
        try:
            new_company = CompanyModel(name=company.name, description=company.description, owner_id=owner_id)
            self.session.add(new_company)
            await self.session.commit()
            await self.session.refresh(new_company)
            return {"company": new_company}
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Company already exists")
        
    async def update_company(self, company_name: str, company_up: CompanyCreateRequestModel, user_id: int) -> dict:
        result = await self.session.execute(select(CompanyModel).filter(CompanyModel.name == company_name))
        company = result.scalars().first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        if user_id != company.owner_id:
            raise HTTPException(status_code=403, detail="Forbidden")
        company.name = company_up.name
        company.description = company_up.description
        try:
            await self.session.commit()
            await self.session.refresh(company)
            return {"name": company.name, "description": company.description}
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Company name already exists")
    
    async def delete_company(self, company_name: str, user_id: int) -> dict:
        result = await self.session.execute(select(CompanyModel).filter(CompanyModel.name == company_name))
        company = result.scalars().first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        if user_id != company.owner_id:
            raise HTTPException(status_code=403, detail="Forbidden")
        await self.session.delete(company)
        await self.session.commit()
        await self.session.close()
        return {"detail" : "Company was deleted", "company" : Company(id=company.id, name=company.name, description=company.description, owner_id=company.owner_id)}
        
    async def get_company(self, company_id: int) -> dict:
        result = await self.session.execute(select(CompanyModel).filter(CompanyModel.id == company_id))
        company = result.scalars().first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        return Company(id=company.id, name=company.name, description=company.description, owner_id=company.owner_id)
        
    async def companies(self) -> dict:
        result = await self.session.execute(select(CompanyModel))
        return {"companies": result.scalars().all()}