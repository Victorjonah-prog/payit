from fastapi import Depends, Request,HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from ..database import engine
from ..models.user import User
from ..auth.jwt import verify_access_tokken
from datetime import datetime

security = HTTPBearer()

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

        async def __call__(self, request: Request):
            credentials: HTTPAuthorizationCredentials= await super(JWTBearer, self).__call__(request)
            if credentials:
                if not credentials.scheme == "Bearer":
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN, detail="invalid authentication scheme"
                    )
                if not self.verify_jwt(credentials.credentials):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN, detail="invalid token or expired"
                    )
                return credentials.credentials
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail ="invalid a"
                )
