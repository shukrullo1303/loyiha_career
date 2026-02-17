"""
Ходим моделлари
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Employee(Base):
    """Ходим модели"""
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    full_name = Column(String(255), nullable=False)
    position = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    passport_number = Column(String(50), nullable=True)
    is_registered = Column(Boolean, default=True)  # Рўйхатдан ўтганми
    is_active = Column(Boolean, default=True)
    hire_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Алокалар
    location = relationship("Location", back_populates="employees")
    faces = relationship("EmployeeFace", back_populates="employee", cascade="all, delete-orphan")
    work_logs = relationship("WorkLog", back_populates="employee", cascade="all, delete-orphan")


class EmployeeFace(Base):
    """Ходим юз маълумотлари"""
    __tablename__ = "employee_faces"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    face_encoding = Column(Text, nullable=False)  # Шифрланган юз маълумоти
    image_path = Column(String(500), nullable=True)
    confidence = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Алокалар
    employee = relationship("Employee", back_populates="faces")


class WorkLog(Base):
    """Иш вақти журнали"""
    __tablename__ = "work_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    check_in = Column(DateTime, nullable=False)
    check_out = Column(DateTime, nullable=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Алокалар
    employee = relationship("Employee", back_populates="work_logs")
