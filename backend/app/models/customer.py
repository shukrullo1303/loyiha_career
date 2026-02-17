"""
Мижоз моделлари
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class CustomerFlow(Base):
    """Мижозлар оқими (кунлик статистика)"""
    __tablename__ = "customer_flows"
    
    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    date = Column(DateTime, nullable=False, index=True)
    total_entered = Column(Integer, default=0)
    total_exited = Column(Integer, default=0)
    peak_hour = Column(Integer, nullable=True)  # Энг кўп мижоз соати
    average_stay_time = Column(Float, nullable=True)  # Минутларда
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Алокалар
    location = relationship("Location", back_populates="customer_flows")
    visits = relationship("CustomerVisit", back_populates="flow", cascade="all, delete-orphan")


class CustomerVisit(Base):
    """Битта мижоз ташрифи"""
    __tablename__ = "customer_visits"
    
    id = Column(Integer, primary_key=True, index=True)
    flow_id = Column(Integer, ForeignKey("customer_flows.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    entered_at = Column(DateTime, nullable=False, index=True)
    exited_at = Column(DateTime, nullable=True)
    stay_duration = Column(Float, nullable=True)  # Минутларда
    track_id = Column(String(100), nullable=True)  # Tracking ID (re-identification учун)
    is_employee = Column(Boolean, default=False)  # Ходимми ёки мижозми
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Алокалар
    flow = relationship("CustomerFlow", back_populates="visits")
