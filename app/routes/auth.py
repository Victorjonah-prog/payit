
from fastapi import APIRouter, FastAPI, status, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import Base, engine
from ..models.user import User
from ..models.auth import LoginRequest, LoginResponse
from datetime import datetime
from ..auth.jwt import create_access_token, verify_password
import logging
import bcrypt
from ..auth.jwt import verify_access_tokken
from ..middlewares.auth import AuthMiddleware


logger = logging.getLogger(__name__)


router = APIRouter(tags=["AUTH"])

@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login(request: LoginRequest, db: Session = Depends(lambda: Session(bind=engine))):
    #check if user exists
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        logger.warning(f"login failed for email: {request.email} - user not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")
    
    password_match= verify_password(request.password, user.password)
    if not password_match:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")

    #generate access token
    claims = { 'sub': str(user.id),
              'email': user.email,
              'user_id': user.id
              }
    
    access_token= create_access_token(claims=claims)

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        email=user.email,
        user_id=user.id
    )
@router.get("/me", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def get_current_user(token: str = Depends(lambda: AuthMiddleware), db: Session= Depends(lambda: Session(bind=engine))):
    payload = verify_access_tokken(token)
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return LoginResponse(
        access_token=token,
        token_type="bearer",
        email=user.email,
        user_id=user.id
    )
    


