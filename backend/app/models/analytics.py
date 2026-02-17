"""
Аналитика моделлари
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Analytics(Base):
    """Аналитика маълумотлари"""
    __tablename__ = "analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    date = Column(DateTime, nullable=False, index=True)
    real_customers = Column(Integer, default=0)  # Реал мижозлар
    reported_revenue = Column(Float, default=0.0)  # Хисоботдаги тушум
    estimated_revenue = Column(Float, default=0.0)  # Тахминий тушум
    average_check = Column(Float, default=0.0)  # Ўртача чек
    discrepancy = Column(Float, default=0.0)  # Тафовут
    discrepancy_percentage = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Алокалар
    location = relationship("Location", back_populates="analytics")


class RiskScore(Base):
    """Риск баҳоси"""
    __tablename__ = "risk_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    date = Column(DateTime, nullable=False, index=True)
    risk_score = Column(Float, default=0.0)  # 0-100
    risk_level = Column(String(50), default="low")  # low, medium, high, critical
    factors = Column(JSON, nullable=True)  # Риск омиллари
    unregistered_employees = Column(Integer, default=0)
    revenue_discrepancy = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Алокалар
    location = relationship("Location", back_populates="risk_scores")


class Heatmap(Base):
    """Юклама харитаси"""
    __tablename__ = "heatmaps"
    
    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    date = Column(DateTime, nullable=False, index=True)
    hour = Column(Integer, nullable=False)  # 0-23
    heatmap_data = Column(JSON, nullable=False)  # Grid маълумотлари
    max_intensity = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
