from typing import Optional

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    username: str  # phone or email
    password: str


class UserBase(BaseModel):
    id: int
    role: str
    phone: Optional[str]
    email: Optional[EmailStr]
    is_active: bool

    class Config:
        orm_mode = True

