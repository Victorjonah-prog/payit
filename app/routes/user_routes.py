from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..database import db_dependency
from ..models.user import User
from typing import List

router = APIRouter()

class UserCreate(BaseModel):
    name: str
    phone: str
    email: str
    password: str
    gender: str
    category: str
    location: str

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    gender: str
    category: str
    location: str

    class Config:
        orm_mode = True

@router.post("/users/", response_model=UserOut)
def create_user(user: UserCreate, db: db_dependency):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/", response_model=List[UserOut])
def read_users(db: db_dependency, skip: int = 0, limit: int = 100):
    users = db.query(User).offset(skip).limit(limit).all()
    return users
