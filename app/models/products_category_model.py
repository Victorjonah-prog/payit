# from .base import Base
# from sqlalchemy import Column, Integer, DateTime, String, func
# from sqlalchemy.orm import relationship

# class ProductCategory(Base):
#     __tablename__ = 'products_category'

#     id = Column(Integer, primary_key=True, nullable=False, index=True)
#     category_name = Column(String(50), min_length=20, max_length=30, unique=True, nullable=False)
#     created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
#     updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

#     products = relationship("Product", back_populates="category")
    