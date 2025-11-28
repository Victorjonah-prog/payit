from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, func, Enum, DECIMAL
from .base import Base
from ..enums import Category
from sqlalchemy.orm import relationship 


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    farmer_id = Column(Integer, ForeignKey('farmers.id'), nullable=False)
    category = Column(Enum(Category), nullable=False)
    status = Column(Enum("available","unavailable"), nullable=False, default="available")
    name = Column(String(30), min_length=3, max_length=30, nullable=False)
    image_url = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    farmer = relationship("Farmer", back_populates="products")
    # category = relationship("ProductCategory", back_populates="products")
    orders = relationship("Order", back_populates="product")



  