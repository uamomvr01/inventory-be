from pydantic import BaseModel, EmailStr
from .users import UserSchema

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class AuthResponse(BaseModel):
    user: UserSchema
    access_token: str
    token_type: str

