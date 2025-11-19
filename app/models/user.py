from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import Enum, DateTime, func
from ..database import Base
from datetime import datetime
from ..enums import Gender, UserCategory


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String(50), nullable=False)
    phone = Column(String(15), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    gender = Column(Enum(Gender.MALE.value, Gender.FEMALE.value), nullable=False)
    category = Column(Enum(UserCategory.BUYER.value, UserCategory.FARMER.value), nullable=False)
    location = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False) 
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False) 
