from fastapi import Depends, Request, status, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from ..database import get_db
from datetime import datetime
from ..auth.jwt import verify_access_token
from ..models.users_model import User
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# HTTPBearer is responsible for extraction of  the bearer token from authorization headers
security = HTTPBearer()

class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error = auto_error)

    async def __call__(self, request: Request, db: Session = Depends(get_db)):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        # Validate credentials
        if credentials:
            if credentials.scheme != 'Bearer':
                self.raiseHttpException("Invalid authorization scheme. expected \'Bearer\'")

            # verify token and get payload
            # user = self.verify_jwt(credentials.credentials, db)
            # if not user:
            #     raiseHttpException("User does not exist!")

            # return user
            return self.verify_jwt(credentials.credentials, db)
        else:
            raiseHttpException("message Invalid or expired token")



    def verify_jwt(self, token: str, db: Session):
        try:
            payload = verify_access_token(token)
            user_id = payload.get('sub')
            if user_id is None:
                return False
            
            user = db.query(User).filter(User.id == user_id).first()

            if not user:
                raiseHttpException("user does not exist!")

            return user

        except Exception as e:
            self.raiseHttpException(f"JWT verification failed. Login session expired: {e}")

    def raiseHttpException(self, e, status=status.HTTP_403_FORBIDDEN):
        raise HTTPException(
            status_code = status,
            detail = {
                "message": e,
                "timestamp": f"{datetime.utcnow()}"
                }
        )


AuthMiddleware = JWTBearer()