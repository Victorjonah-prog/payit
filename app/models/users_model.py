from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, func, Enum
from .base import Base
from ..enums import Gender
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False,index=False)
    name = Column(String(50), min_length=20, max_length=50, nullable=False)
    phone = Column(String(15), min_length=11, max_length=15, nullable=True, unique=True)
    email= Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(100), nullable=True)
    gender = Column(Enum(Gender), nullable=True)
    location = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=True)

    farmer= relationship("Farmer", back_populates="user")
    buyer= relationship("Buyer", back_populates="user")