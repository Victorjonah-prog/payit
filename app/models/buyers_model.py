from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, func
from .base import Base

class Buyer(Base):
    __tablename__ = 'buyers'

    id = Column(Integer, primary_key=True, nullable=False,index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
