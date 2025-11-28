from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, func
from .base import Base
from sqlalchemy.orm import relationship

class Farmer(Base):
    __tablename__ = 'farmers'

    id = Column(Integer, primary_key=True, nullable=False,index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    products = relationship("Product", back_populates="farmer")
    user = relationship("User", back_populates="farmer")

