from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,DECIMAL
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import Enum, DateTime, func
from ..database import Base
from datetime import datetime

class Products(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True,)
    name = Column(String(50), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    category = Column(Enum('grains', 'tubers', 'vegetable','fruits','livestock','cereals','oils','latex'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False) 
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False) 