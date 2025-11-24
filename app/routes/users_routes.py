from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import APIRouter, HTTPException, status, Depends
from ..models import users_model
from ..schemas.users_schema import User, UserResponse
from ..middlewares.auth import AuthMiddleware
from datetime import datetime
from typing import List
import logging
import bcrypt
import pymysql

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)



# router = APIRouter()



# @router.post("/users")
# def create_user(user: User, db: Session = Depends(get_db)):
#     if db.query(users_model.User).filter(users_model.User.email == user.email).first():
#         raise HTTPException(
#             status_code = status.HTTP_409_CONFLICT,
#             detail = "User email already exists!"
#         )

#     salts = bcrypt.gensalt(rounds=12)
#     hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), salts)

#     new_user = users_model.User(
#         **user.model_dump(exclude={"password"}),
#         password=hashed_password.decode()
#     )

#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return(new_user)


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_current_user(current_user = Depends(AuthMiddleware), db: Session = Depends(get_db)):
    return current_user

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create(user_request: User, db: Session = Depends(get_db)):

    userExists = db.query(users_model.User).filter(
        (user_request.email == users_model.User.email) | (user_request.phone == users_model.User.phone)
    ).first()

    if userExists:
        raiseError("email or phone already exists")
    
    salts = bcrypt.gensalt(rounds=12)
    hashed_password = bcrypt.hashpw(user_request.password.encode('utf-8'), salts)
    
    new_user = users_model.User(
        **user_request.dict(exclude={"password", "confirm_password", "gender", "category"}),
        password=hashed_password.decode(),
        gender = user_request.gender.value
    )

    try:  
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    except pymysql.DataError as e:
        raiseError(e)
    except Exception as e:
        raiseError(e)

def raiseError(e):
    logger.error(f"failed to create record error: {e}")
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail = {
            "status": "error",
            "message": f"failed to create user: {e}",
            "timestamp": f"{datetime.utcnow()}"
        }
    )



@router.get("/users/{user_id}")
def get_a_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(users_model.User).filter(users_models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User with ID not found"
        )

    return user

@router.put("/users")
def update_user(current_user: int, user: User, db: Session = Depends(get_db)):
    updated_user = db.query(users_model.User).filter(users_models.User.id == current_user.id).first()
    if not update_user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User with ID not found"
        )

    for field, value in user.dict().items():
        setattr(updated_user, field, value)

    db.commit()
    db.refresh(updated_user)
    return updated_user

@router.delete("/users")
def delete_user(current_user = Depends(AuthMiddleware), db: Session = Depends(get_db)):
    user_to_delete = db.query(users_model.User).filter(users_model.User.id == current_user.id).first()
    if not user_to_delete:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User with ID not found"
        )


    db.delete(user_to_delete)
    db.commit()
    raise HTTPException(
        status_code = status.HTTP_204_NO_CONTENT,
        detail = "User deleted successfully"
    )

@router.get("/users", response_model=List[UserResponse])
def get_all_users(db: Session=Depends(get_db)):
    return db.query(users_model.User).all()
