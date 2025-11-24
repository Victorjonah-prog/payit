import os
from jose import jwt, JWTError
from typing import Optional
from datetime import timedelta, datetime

SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ACCESS_TOKEN_EXPIRATION_IN_MINUTES = int(os.getenv('JWT_EXPIRATION_TIME'))
ALGORITHM = os.getenv('JWT_ALGORITHM')


# def verify_password(plain_text_password: str, hashed_password: str)-> bool: MOVED TO ROUTES AUTH
#     plain_text_password = plain_text_password.encode('utf-8')

#     return bcrypt.checkpw(plain_text_password, hashed_password)

# Test verification
# plain_text_password = 'password'

# salts = bcrypt.gensalt(rounds=12)
# hashed_password = bcrypt.hashpw(plain_text_password.encode('utf-8'), salts)
# print(verify_password(plain_text_password, hashed_password))

# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None)-> str:
#     data_to_encode = data.copy()
#     try:
#         if expires_delta:
#             expiration_time = datetime.utcnow() + expires_delta
#         else:
#             expiration_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_IN_MINUTES)
    
#         data_to_encode.update({'exp': expiration_time})

#         return jwt.encode(data_to_encode, SECRET_KEY, ALGORITHM)
#     except JWTError as e:
#         raise e

#     def verify_access_token(token: str):
#         try:
#             return jwt.decode(token, SECRET_KEY, ALGORITHM)
#         except JWTError as e:
#             raise

    # OR encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, ALGORITHM)

# Refactored
def create_access_token(claims: dict, expires_delta: Optional[timedelta] = None)-> str:
    try:
        if expires_delta:
            expiration_time = datetime.utcnow() + expires_delta
        else:
            expiration_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_IN_MINUTES)
            
        claims.update({'exp': expiration_time})
            
        return jwt.encode(claims, SECRET_KEY, ALGORITHM)
    except JWTError as e:
            raise e

def verify_access_token(token: str):
        try:
            return jwt.decode(token, SECRET_KEY, ALGORITHM)
        except JWTError as e:
            raise