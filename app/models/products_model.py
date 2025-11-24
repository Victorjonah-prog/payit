from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, func, Enum, DECIMAL
from .base import Base
from ..enums import Category

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    farmer_id = Column(Integer, ForeignKey('farmers.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('products_category.id'), nullable=False)
    name = Column(String(30), min_length=3, max_length=30, nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
  