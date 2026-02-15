"""
Ходим схемалари
"""
from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


class EmployeeBase(BaseModel):
    """Асосий ходим схемаси"""
    full_name: str
    position: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    passport_number: Optional[str] = None
    is_registered: bool = True
    hire_date: Optional[date] = None


class EmployeeCreate(EmployeeBase):
    """Ходим яратиш схемаси"""
    location_id: int


class EmployeeUpdate(BaseModel):
    """Ходим янгилаш схемаси"""
    full_name: Optional[str] = None
    position: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    is_registered: Optional[bool] = None
    is_active: Optional[bool] = None


class EmployeeFaceCreate(BaseModel):
    """Ходим юзини яратиш схемаси"""
    employee_id: int
    image_base64: str  # Base64 encoded image


class Employee(EmployeeBase):
    """Ходим жавоб схемаси"""
    id: int
    location_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
