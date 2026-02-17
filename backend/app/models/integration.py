"""
Интеграция моделлари
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class TaxIntegration(Base):
    """Солиқ интеграцияси"""
    __tablename__ = "tax_integrations"
    
    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    tax_id = Column(String(50), nullable=False)
    last_sync = Column(DateTime, nullable=True)
    reported_revenue = Column(Float, default=0.0)
    tax_paid = Column(Float, default=0.0)
    sync_status = Column(String(50), default="pending")  # pending, success, error
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class KKTIntegration(Base):
    """ККТ (онлайн касса) интеграцияси"""
    __tablename__ = "kkt_integrations"
    
    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    kkt_serial = Column(String(100), nullable=False)
    kkt_number = Column(String(100), nullable=True)
    last_sync = Column(DateTime, nullable=True)
    total_receipts = Column(Integer, default=0)
    total_amount = Column(Float, default=0.0)
    sync_status = Column(String(50), default="pending")
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
