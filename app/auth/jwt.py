from jose import JWTError,jwt
from datetime import timedelta, datetime
import bcrypt
import os 
from typing import Dict, Optional

SECRET_KEY=os.getenv('JWT_SECRET_KEY', '97801b050076d72d348b039d6c83293f50b66a928f83c39e6b8ce70347fdc6ea')
ALGORITHM=os.getenv('JWT_ALGORITHM', 'HS256')

ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv('JWT_EXPIRATION_TIME', '30'))

def verify_password(plain_text_password: str, hashed_password: str) -> bool:
    plain_text_password=plain_text_password.encode('utf-8')

    return bcrypt.checkpw(plain_text_password, hashed_password.encode('utf-8'))

def create_access_token(claims: dict, expires_delta: Optional[timedelta]=None) -> str:
   

    if expires_delta:
        expiration_time = datetime.utcnow() + expires_delta
    else:
        expiration_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    claims.update({'exp':expiration_time})

    return jwt.encode(claims, SECRET_KEY,ALGORITHM)

def verify_access_tokken(token: str):
    try:
        return jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    except JWTError as e:
        raise 
