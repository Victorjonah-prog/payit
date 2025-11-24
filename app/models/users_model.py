from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, func, Enum
from .base import Base
from ..enums import Gender

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False,index=True)
    name = Column(String(50), min_length=20, max_length=50, nullable=False)
    phone = Column(String(15), min_length=11, max_length=15, nullable=False, unique=True)
    email= Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(100), nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    location = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)