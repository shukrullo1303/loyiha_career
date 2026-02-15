"""
Мижоз схемалари
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CustomerVisitBase(BaseModel):
    """Асосий мижоз ташрифи схемаси"""
    entered_at: datetime
    exited_at: Optional[datetime] = None
    stay_duration: Optional[float] = None


class CustomerVisit(CustomerVisitBase):
    """Мижоз ташрифи жавоб схемаси"""
    id: int
    flow_id: int
    location_id: int
    track_id: Optional[str] = None
    is_employee: bool = False
    employee_id: Optional[int] = None
    
    class Config:
        from_attributes = True


class CustomerFlowBase(BaseModel):
    """Асосий мижозлар оқими схемаси"""
    date: datetime
    total_entered: int = 0
    total_exited: int = 0
    peak_hour: Optional[int] = None
    average_stay_time: Optional[float] = None


class CustomerFlow(CustomerFlowBase):
    """Мижозлар оқими жавоб схемаси"""
    id: int
    location_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
