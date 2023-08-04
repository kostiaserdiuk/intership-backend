from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from app.db.db import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(100), unique=True)
    password = Column(String(255))
    # companies = relationship("Company", back_populates="owner", foreign_keys="Company.owner_id")
    companies = relationship("Company", back_populates="owner")
    # requested_companies = relationship("Company", back_populates="join_request", foreign_keys="Company.join_requests_id")
    actions = relationship("CompanyAction", back_populates="user")
    join_request = relationship("UserAction", back_populates="user")
    employees = relationship("Employees", back_populates="user")


class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    description = Column(String(255))
    owner_id = Column(Integer, ForeignKey('users.id'))
    # owner = relationship("User", back_populates="companies", foreign_keys=[owner_id])
    owner = relationship("User", back_populates="companies")
    action_invite = relationship("CompanyAction", back_populates="company")
    join_request = relationship("UserAction", back_populates="company")
    employees = relationship("Employees", back_populates="company")
    quizzes = relationship("Quiz", back_populates="company")


class CompanyAction(Base):
    __tablename__ = 'company_actions'
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'))
    invite_user = Column(Integer, ForeignKey('users.id'))
    # invited_users = Column(ARRAY(Integer, dimensions=None), default=[])
    company = relationship("Company", back_populates="action_invite")
    user = relationship("User", back_populates="actions")

class UserAction(Base):
    __tablename__ = 'user_actions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    join_request = Column(Integer, ForeignKey('companies.id'))
    user = relationship("User", back_populates="join_request")
    company = relationship("Company", back_populates="join_request")

class Employees(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    is_admin = Column(Boolean, default=False)
    user = relationship("User", back_populates="employees")
    company = relationship("Company", back_populates="employees")

class Quiz(Base):
    __tablename__ = 'quizzes'
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'))
    name = Column(String(50), unique=True)
    description = Column(String(255))
    frequency = Column(Integer)
    questions = Column(JSON)
    company = relationship("Company", back_populates="quizzes")
