from pydantic import BaseModel, Field, EmailStr, field_validator
import re

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field( min_length=6, max_length=10)
    

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
    
class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    email: EmailStr
    user_id: int