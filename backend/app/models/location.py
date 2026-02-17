"""
Локация ва камера моделлари
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base


class LocationType(str, enum.Enum):
    """Локация тури"""
    CAFE = "cafe"
    RESTAURANT = "restaurant"
    TEA_HOUSE = "tea_house"
    HAIR_SALON = "hair_salon"
    CAR_WASH = "car_wash"
    SERVICE_CENTER = "service_center"
    HOUSEHOLD_SERVICE = "household_service"
    OTHER = "other"


class Location(Base):
    """Локация модели"""
    __tablename__ = "locations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(String(500), nullable=False)
    location_type = Column(Enum(LocationType), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    tax_id = Column(String(50), unique=True, nullable=True)  # ИНН
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Алокалар
    owner = relationship("User", back_populates="locations")
    cameras = relationship("Camera", back_populates="location", cascade="all, delete-orphan")
    employees = relationship("Employee", back_populates="location", cascade="all, delete-orphan")
    customer_flows = relationship("CustomerFlow", back_populates="location", cascade="all, delete-orphan")
    analytics = relationship("Analytics", back_populates="location", cascade="all, delete-orphan")
    risk_scores = relationship("RiskScore", back_populates="location", cascade="all, delete-orphan")


class Camera(Base):
    """Камера модели"""
    __tablename__ = "cameras"
    
    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    name = Column(String(255), nullable=False)
    ip_address = Column(String(50), nullable=False)
    port = Column(Integer, default=80)
    username = Column(String(100), nullable=True)
    password = Column(String(255), nullable=True)  # Шифрланган
    onvif_url = Column(String(500), nullable=True)
    camera_type = Column(String(50), default="entrance")  # entrance, exit, internal
    is_active = Column(Boolean, default=True)
    stream_url = Column(String(500), nullable=True)
    resolution = Column(String(50), default="1920x1080")
    fps = Column(Integer, default=30)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Алокалар
    location = relationship("Location", back_populates="cameras")
