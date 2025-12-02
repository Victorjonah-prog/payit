from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import APIRouter, HTTPException, status, Depends, Request
from ..schemas.users_schema import User, UserResponse
from ..middlewares.auth import AuthMiddleware
from datetime import datetime
from typing import List
import logging
import bcrypt
import pymysql
from ..config.oauth import oauth
from ..enums import Gender, Category
from ..auth.jwt import create_access_token
from fastapi.responses import RedirectResponse
from ..config.oauth import  AUTH0_DOMAIN, AUTH0_CLIENT_ID 
from ..models.users_model import User
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/oauth",
    tags=["Oauth"]
)



@router.get("/login")
async def login(request: Request):
     
    redirect_uri = "http://localhost:8000/oauth/callback"
    
    try:
        return await oauth.auth0.authorize_redirect(request, redirect_uri=redirect_uri)
    except Exception as e:
        print("Login error:", e)  
        raise HTTPException(status_code=400, detail=f"Cannot connect to login page: {e}")


@router.get("/callback", name="callback")
async def callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.auth0.authorize_access_token(request)
        print("Full token:", token)

        
        user_info = token.get("userinfo")
        print("User info", user_info)

        email = user_info.get("email")

        if not email:
            github_id = user_info["sub"].split("|")[1]   
            email = f"{github_id}@users.noreply.github.com"   
            print(f"GitHub email is : {email}")
        
        name = user_info.get("name") or user_info.get("nickname") or "User"

        
        user = db.query(User).filter(User.email == email).first()  

        
        if not user:
            user = User(                                      
                name=name,
                email=email,
                phone="09159376459",
                password="social-login", 
                gender=Gender.M.value,

                location="jos"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print("New user created:", email)

        
        jwt = create_access_token({
            "sub": str(user.id),
            "email": user.email,
            "user_id": str(user.id)
        })

        return {
            "access_token": jwt,
            "email": user.email,
            "id": user.id,
            "message": "Login successful!"
        }

    except Exception as e:
        print("CALLBACK ERROR:", e)  
        raise HTTPException(status_code=400, detail=f"Login failed: {str(e)}")
    
# @router.get("/logout")
# def logout(request: Request):
#     return_uri = "http://localhost:8000"

#     logout_url =(
#         f"https://{AUTH0_DOMAIN}/v2/logout"
#         f"client_id={AUTH0_CLIENT_ID}&"
#         f"return_to={return_uri}"
#     )
#     return RedirectResponse(url=logout_url)



@router.get("/logout")
def logout(request: Request):
    return_uri = "http://localhost:8000"
    
    params = {
        "client_id": AUTH0_CLIENT_ID,
        "returnTo": return_uri
    }
    
    logout_url = f"https://{AUTH0_DOMAIN}/v2/logout?{urlencode(params)}"
    
    print(f"Logout URL: {logout_url}")  
    return RedirectResponse(url=logout_url)



