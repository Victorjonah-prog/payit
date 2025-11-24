from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, func, DECIMAL, Enum
from ..enums import OrderStatus
from .base import Base

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, nullable=False,index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    buyer_id = Column(Integer, ForeignKey('buyers.id'), nullable=False)
    unit_price = Column(DECIMAL, nullable=False)
    quantity = Column(Integer, nullable=False)
    order_status = Column(Enum(OrderStatus), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
