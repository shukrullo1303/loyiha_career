"""
Фойдаланувчи схемалари
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from app.models.user import UserRole


class UserBase(BaseModel):
    """Асосий фойдаланувчи схемаси"""
    username: str
    email: EmailStr
    full_name: str
    role: UserRole


class UserCreate(UserBase):
    """Фойдаланувчи яратиш схемаси"""
    password: str


class UserUpdate(BaseModel):
    """Фойдаланувчи янгилаш схемаси"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class User(UserBase):
    """Фойдаланувчи жавоб схемаси"""
    id: int
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Токен схемаси"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Токен маълумотлари"""
    username: Optional[str] = None
