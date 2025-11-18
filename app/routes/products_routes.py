from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..database import db_dependency
from ..models.producs import product
from typing import List

router = APIRouter()


class UserCreate(BaseModel):
    name: str
    price: float
    quantity: int
    category: str
    

    class config:
        orm_mode = True

@router.post("/products/", response_model=UserCreate)
def create_product(product: UserCreate, db: db_dependency):
    db_product = db.query(product).filter(product.name == product.name).first()
    if db_product:
        raise HTTPException(status_code=400, detail="product already registered")
    db_product = product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product



