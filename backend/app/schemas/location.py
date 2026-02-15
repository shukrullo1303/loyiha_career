"""
Локация схемалари
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.models.location import LocationType


class LocationBase(BaseModel):
    """Асосий локация схемаси"""
    name: str
    address: str
    location_type: LocationType
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    tax_id: Optional[str] = None


class LocationCreate(LocationBase):
    """Локация яратиш схемаси"""
    pass


class LocationUpdate(BaseModel):
    """Локация янгилаш схемаси"""
    name: Optional[str] = None
    address: Optional[str] = None
    location_type: Optional[LocationType] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_active: Optional[bool] = None


class Location(LocationBase):
    """Локация жавоб схемаси"""
    id: int
    owner_id: Optional[int] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
