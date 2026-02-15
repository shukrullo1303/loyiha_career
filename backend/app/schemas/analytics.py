"""
Аналитика схемалари
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any


class AnalyticsBase(BaseModel):
    """Асосий аналитика схемаси"""
    date: datetime
    real_customers: int = 0
    reported_revenue: float = 0.0
    estimated_revenue: float = 0.0
    average_check: float = 0.0
    discrepancy: float = 0.0
    discrepancy_percentage: float = 0.0


class Analytics(AnalyticsBase):
    """Аналитика жавоб схемаси"""
    id: int
    location_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class RiskScoreBase(BaseModel):
    """Асосий риск баҳоси схемаси"""
    date: datetime
    risk_score: float = 0.0
    risk_level: str = "low"
    factors: Optional[Dict[str, Any]] = None
    unregistered_employees: int = 0
    revenue_discrepancy: float = 0.0


class RiskScore(RiskScoreBase):
    """Риск баҳоси жавоб схемаси"""
    id: int
    location_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class HeatmapBase(BaseModel):
    """Асосий юклама харитаси схемаси"""
    date: datetime
    hour: int
    heatmap_data: Dict[str, Any]
    max_intensity: int = 0


class Heatmap(HeatmapBase):
    """Юклама харитаси жавоб схемаси"""
    id: int
    location_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
