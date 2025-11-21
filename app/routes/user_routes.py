from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..database import db_dependency
from ..models.user import User
from typing import List
import bcrypt
from pydantic import BaseModel, Field, EmailStr, field_validator
from ..enums import Gender, UserCategory
import re


router = APIRouter()

class UserCreate(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    phone: str = Field(max_length=15,min_length=11, pattern= r"^0[0-9]{10}$")
    email: str = EmailStr
    password: str = Field(
        min_length=6,
        max_length=10)
    gender: str
    category: str
    location: str = Field()

    @field_validator('phone')
    def phone_must_be_valid(cls, value):
        if value.isdigit() is not True:
            raise ValueError('phone number must be only digits')
        return value

    @field_validator('password')
    def password_complexity(cls, value):
        if not re.search(r'[A-Z]', value):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', value):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', value):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[\W_]', value):
            raise ValueError('Password must contain at least one special character')
        return value

class UserOut(BaseModel):
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
    salts= bcrypt.gensalt(rounds=12)
    hashed_passwords= bcrypt.hashpw(user.password.encode('utf-8'),salts)
    user.password= hashed_passwords.decode('utf-8')
    db_user_by_email = db.query(User).filter(User.email == user.email).first()
    if db_user_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user_by_phone = db.query(User).filter(User.phone == user.phone).first()
    if db_user_by_phone:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    
    user_data = user.dict()
    user_data['gender'] = Gender(user_data['gender'])
    user_data['category'] = UserCategory(user_data['category'])
    
    db_user = User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/", response_model=List[UserOut])
def read_users(db: db_dependency, skip: int = 0, limit: int = 100):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.get("/users/{user_id}", response_model=UserOut)
def get_user_by_id(user_id: int, db: db_dependency):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return db_user

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: db_dependency):
    db_user= db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    db.delete(db_user)
    db.commit()
    db.refresh(db_user)
    return {"detail": "user deleted successfully"}

@router.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserCreate, db: db_dependency):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    for key, value in user.dict().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user