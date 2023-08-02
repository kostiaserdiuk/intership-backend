from app.db.db import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.models import Company, User, CompanyAction, Employees, UserAction

class CompanyActions:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def invite(self, company_id: int, user_id: int, current_user: int):
        result = await self.session.execute(select(Company).filter(Company.id == company_id))
        company = result.scalars().first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        if company.owner_id != current_user:
            raise HTTPException(status_code=403, detail="You are not the owner of this company")
        result = await self.session.execute(select(User).filter(User.id == user_id))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        try:
            result = await self.session.execute(select(CompanyAction).filter(CompanyAction.company_id == company_id, CompanyAction.invite_user == user_id))
            if result.scalars().first() is not None:
                return {"status": "error", "detail": "User already invited"}
            new_invite = CompanyAction(company_id=company_id, invite_user=user_id)
            self.session.add(new_invite)
            await self.session.commit()
            await self.session.refresh(company)
            return {"status": "success", "detail": "User invited"}
        except IntegrityError:
            return {"status": "error", "detail": "User already invited"}
    
    async def reject_invite(self, company_id: int, user_id: int, current_user: int):
        result = await self.session.execute(select(Company).filter(Company.id == company_id))
        company = result.scalars().first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        if company.owner_id != current_user:
            raise HTTPException(status_code=403, detail="You are not the owner of this company")
        result = await self.session.execute(select(CompanyAction).filter(CompanyAction.company_id == company_id, CompanyAction.invite_user == user_id))
        invite = result.scalars().first()
        if not invite:
            raise HTTPException(status_code=404, detail="Invite not found")
        try:
            await self.session.delete(invite)
            await self.session.commit()
            await self.session.close()
            return {"status": "success", "detail": "Invite rejected"}
        except IntegrityError:
            return {"status": "error", "detail": "Invite already rejected"}
    
    async def accept_request(self, company_id: int, user_id: int, current_user: int):
        result = await self.session.execute(select(UserAction).filter(UserAction.join_request == company_id, UserAction.user_id == user_id))
        request = result.scalars().first()
        if not request:
            raise HTTPException(status_code=404, detail="Request not found")
        result = await self.session.execute(select(Company).filter(Company.id == company_id))
        company = result.scalars().first()
        if company.owner_id != current_user:
            raise HTTPException(status_code=403, detail="You are not the owner of this company")
        try:
            new_employee = Employees(company_id=company_id, user_id=user_id)
            self.session.add(new_employee)
            await self.session.delete(request)
            await self.session.commit()
            await self.session.close()
            return {"status": "success", "detail": "Request accepted"}
        except IntegrityError:
            return {"status": "error", "detail": "Request already accepted"}
    
    async def decline_request(self, company_id: int, user_id: int, current_user: int):
        result = await self.session.execute(select(UserAction).filter(UserAction.join_request == company_id, UserAction.user_id == user_id))
        request = result.scalars().first()
        if not request:
            raise HTTPException(status_code=404, detail="Request not found")
        result = await self.session.execute(select(Company).filter(Company.id == company_id))
        company = result.scalars().first()
        if company.owner_id != current_user:
            raise HTTPException(status_code=403, detail="You are not the owner of this company")
        try:
            await self.session.delete(request)
            await self.session.commit()
            await self.session.close()
            return {"status": "success", "detail": "Request declined"}
        except IntegrityError:
            return {"status": "error", "detail": "Request already declined"}
    
    async def kick(self, company_id: int, user_id: int, current_user: int):
        result = await self.session.execute(select(Company).filter(Company.id == company_id))
        company = result.scalars().first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        if company.owner_id != current_user:
            raise HTTPException(status_code=403, detail="You are not the owner of this company")
        try:
            result = await self.session.execute(select(Employees).filter(Employees.company_id == company_id, Employees.user_id == user_id))
            employee = result.scalars().first()
            if employee is None:
                return {"status": "error", "detail": "User is not an employee"}
            await self.session.delete(employee)
            await self.session.commit()
            await self.session.close()
            return {"status": "success", "detail": "User kicked"}
        except IntegrityError:
            return {"status": "error", "detail": "User already kicked"}
        
    async def invited(self, company_id: int, current_user: int):
        result = await self.session.execute(select(Company).filter(Company.id == company_id))
        company = result.scalars().first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        if company.owner_id != current_user:
            raise HTTPException(status_code=403, detail="You are not the owner of this company")
        result = await self.session.execute(select(CompanyAction).filter(CompanyAction.company_id == company_id))
        invites = result.scalars().all()
        if not invites:
            return {"status": "success", "detail": "No invited users"}
        return {"status": "success", "invites": invites}
    
    async def requests(self, company_id: int, current_user: int):
        result = await self.session.execute(select(Company).filter(Company.id == company_id))
        company = result.scalars().first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        if company.owner_id != current_user:
            raise HTTPException(status_code=403, detail="You are not the owner of this company")
        result = await self.session.execute(select(UserAction).filter(UserAction.join_request == company_id))
        requests = result.scalars().all()
        if not requests:
            return {"status": "success", "detail": "No join requests"}
        return {"status": "success", "requests": requests}
    
    async def employees(self, company_id: int, current_user: int):
        result = await self.session.execute(select(Company).filter(Company.id == company_id))
        company = result.scalars().first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        if company.owner_id != current_user:
            raise HTTPException(status_code=403, detail="You are not the owner of this company")
        result = await self.session.execute(select(Employees).filter(Employees.company_id == company_id))
        employees = result.scalars().all()
        if not employees:
            return {"status": "success", "detail": "No employees"}
        return {"status": "success", "employees": employees}
    
    async def assign_admin(self, company_id: int, user_id: int, current_user: int):
        result = await self.session.execute(select(Company).filter(Company.id == company_id))
        company = result.scalars().first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        if company.owner_id != current_user:
            raise HTTPException(status_code=403, detail="You are not the owner of this company")
        try:
            result = await self.session.execute(select(Employees).filter(Employees.company_id == company_id, Employees.user_id == user_id))
            employee = result.scalars().first()
            if employee is None:
                return {"status": "error", "detail": "User is not an employee"}
            employee.is_admin = True
            await self.session.commit()
            await self.session.close()
            return {"status": "success", "detail": "User assigned as admin"}
        except IntegrityError:
            return {"status": "error", "detail": "User already admin"}
    
    async def unassign_admin(self, company_id: int, user_id: int, current_user: int):
        result = await self.session.execute(select(Company).filter(Company.id == company_id))
        company = result.scalars().first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        if company.owner_id != current_user:
            raise HTTPException(status_code=403, detail="You are not the owner of this company")
        try:
            result = await self.session.execute(select(Employees).filter(Employees.company_id == company_id, Employees.user_id == user_id))
            employee = result.scalars().first()
            if employee is None:
                return {"status": "error", "detail": "User is not an employee"}
            employee.is_admin = False
            await self.session.commit()
            await self.session.close()
            return {"status": "success", "detail": "User unassigned as admin"}
        except IntegrityError:
            return {"status": "error", "detail": "User already not admin"}
    
    async def get_admins(self, company_id: int, current_user: int):
        result = await self.session.execute(select(Company).filter(Company.id == company_id))
        company = result.scalars().first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        if company.owner_id != current_user:
            raise HTTPException(status_code=403, detail="You are not the owner of this company")
        result = await self.session.execute(select(Employees).filter(Employees.company_id == company_id, Employees.is_admin == True))
        admins =  result.scalars().all()
        if not admins:
            return {"status": "success", "detail": "No admins"}
        return {"status": "success", "admins": admins}
            
class UserActions:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def accept_invite(self, company_id: int, user_id: int):
        result = await self.session.execute(select(CompanyAction).filter(CompanyAction.company_id == company_id, CompanyAction.invite_user == user_id))
        invite = result.scalars().first()
        if not invite:
            raise HTTPException(status_code=404, detail="Invite not found")
        try:
            new_employee = Employees(company_id=company_id, user_id=user_id)
            self.session.add(new_employee)
            await self.session.commit()
            await self.session.refresh(new_employee)
            await self.session.delete(invite)
            await self.session.commit()
            await self.session.close()
            return {"status": "success", "detail": "Invite accepted"}
        except IntegrityError:
            return {"status": "error", "detail": "Invite already accepted"}
    
    async def decline_invite(self, company_id: int, user_id: int):
        result = await self.session.execute(select(CompanyAction).filter(CompanyAction.company_id == company_id, CompanyAction.invite_user == user_id))
        invite = result.scalars().first()
        if not invite:
            raise HTTPException(status_code=404, detail="Invite not found")
        try:
            await self.session.delete(invite)
            await self.session.commit()
            await self.session.close()
            return {"status": "success", "detail": "Invite declined"}
        except IntegrityError:
            return {"status": "error", "detail": "Invite already declined"}
    
    async def request_to_company(self, company_id: int, user_id: int):
        result = await self.session.execute(select(Company).filter(Company.id == company_id))
        company = result.scalars().first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        try:
            result = await self.session.execute(select(UserAction).filter(UserAction.join_request == company_id, UserAction.user_id == user_id))
            if result.scalars().first() is not None:
                return {"status": "error", "detail": "User already requested"}
            new_request = UserAction(join_request=company_id, user_id=user_id)
            self.session.add(new_request)
            await self.session.commit()
            await self.session.refresh(company)
            return {"status": "success", "detail": "Request sent"}
        except IntegrityError:
            return {"status": "error", "detail": "User already requested"}
    
    async def cancel_request(self, company_id: int, user_id: int):
        result = await self.session.execute(select(UserAction).filter(UserAction.join_request == company_id, UserAction.user_id == user_id))
        request = result.scalars().first()
        if not request:
            raise HTTPException(status_code=404, detail="Request not found")
        try:
            await self.session.delete(request)
            await self.session.commit()
            await self.session.close()
            return {"status": "success", "detail": "Request canceled"}
        except IntegrityError:
            return {"status": "error", "detail": "Request already canceled"}
        
    async def leave_company(self, company_id: int, user_id: int):
        result = await self.session.execute(select(Company).filter(Company.id == company_id))
        company = result.scalars().first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        try:
            result = await self.session.execute(select(Employees).filter(Employees.company_id == company_id, Employees.user_id == user_id))
            company = result.scalars().first()
            if company is None:
                return {"status": "error", "detail": "User is not an employee"}
            await self.session.delete(company)
            await self.session.commit()
            await self.session.close()
            return {"status": "success", "detail": "User left"}
        except IntegrityError:
            return {"status": "error", "detail": "User already left"}
        
    async def invites(self, user_id: int):
        result = await self.session.execute(select(CompanyAction).filter(CompanyAction.invite_user == user_id))
        invites = result.scalars().all()
        if not invites:
            return {"status": "success", "detail": "No invites"}
        return {"status": "success", "detail": invites}
    
    async def requests(self, user_id: int):
        result = await self.session.execute(select(UserAction).filter(UserAction.user_id == user_id))
        requests = result.scalars().all()
        if not requests:
            return {"status": "success", "detail": "No requests"}
        return {"status": "success", "detail": requests}