from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import APIRouter, HTTPException, status, Depends
from ..models import users_model
from ..auth.jwt import create_access_token
from ..schemas.auth import LoginRequest, LoginResponse
from datetime import datetime
# from typing import List
import logging
import bcrypt

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)



# router = APIRouter()




@router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
def login(login_request: LoginRequest, db: Session = Depends(get_db)):

    userExists = db.query(users_model.User).filter(login_request.email == users_model.User.email).first()

    if not userExists:
        raiseHttpException("email does not exists")

    password_match = verify_password(login_request.password, userExists.password)

    if not password_match:
        raiseHttpException('Invalid password')


    claims = {
        'sub': str(userExists.id),
        'email': userExists.email,
        'user_id': str(userExists.id)
    }

    access_token = create_access_token(claims)

    return LoginResponse(
        access_token = access_token,
        token_type = 'bearer',
        email = userExists.email,
        user_id = userExists.id
    )
    



# HELPER FUNCTIONS
def verify_password(plain_text_password: str, hashed_password: str)-> bool:
    # plain_text_password = plain_text_password.encode('utf-8')

    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))

def raiseHttpException(e, status=status.HTTP_401_UNAUTHORIZED):
    logger.error(f"failed to create record error: {e}")
    raise HTTPException(
        status_code = status,
        detail = {
            "status": "error",
            "message": f"failed to create user: {e}",
            "timestamp": f"{datetime.utcnow()}"
        }
    )






