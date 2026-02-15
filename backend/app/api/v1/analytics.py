"""
Аналитика API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.analytics import Analytics, RiskScore, Heatmap
from app.schemas.analytics import (
    Analytics as AnalyticsSchema,
    RiskScore as RiskScoreSchema,
    Heatmap as HeatmapSchema
)
from app.services.predictive_analytics_service import PredictiveAnalyticsService
from app.services.risk_scoring_service import RiskScoringService
from app.services.video_analytics_service import VideoAnalyticsService

router = APIRouter()
predictive_service = PredictiveAnalyticsService()
risk_service = RiskScoringService()
video_service = VideoAnalyticsService()


@router.get("/locations/{location_id}", response_model=List[AnalyticsSchema])
async def get_location_analytics(
    location_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Локация аналитикаси"""
    query = db.query(Analytics).filter(Analytics.location_id == location_id)
    
    if start_date:
        query = query.filter(Analytics.date >= start_date)
    if end_date:
        query = query.filter(Analytics.date <= end_date)
    
    analytics = query.order_by(Analytics.date.desc()).all()
    return analytics


@router.get("/locations/{location_id}/risk", response_model=RiskScoreSchema)
async def get_location_risk(
    location_id: int,
    date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Локация риск баҳоси"""
    if not date:
        date = datetime.utcnow()
    
    # Базадан олиш ёки ҳисоблаш
    risk_score = db.query(RiskScore).filter(
        RiskScore.location_id == location_id,
        RiskScore.date >= date - timedelta(days=1),
        RiskScore.date < date + timedelta(days=1)
    ).first()
    
    if not risk_score:
        # Янги ҳисоблаш
        result = await risk_service.calculate_risk_score(location_id, date)
        risk_score = db.query(RiskScore).filter(
            RiskScore.location_id == location_id,
            RiskScore.date >= date - timedelta(days=1)
        ).order_by(RiskScore.date.desc()).first()
    
    if not risk_score:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Риск баҳоси топилмади"
        )
    
    return risk_score


@router.get("/locations/{location_id}/predictions")
async def get_predictions(
    location_id: int,
    days: int = 30,
    current_user: User = Depends(get_current_user)
):
    """Келгуси прогнозлар"""
    predictions = await predictive_service.get_predictions(location_id, days)
    return predictions


@router.get("/locations/{location_id}/heatmap", response_model=HeatmapSchema)
async def get_heatmap(
    location_id: int,
    date: datetime,
    hour: Optional[int] = None,
    current_user: User = Depends(get_current_user)
):
    """Юклама харитаси"""
    heatmap = await video_service.get_heatmap(location_id, date.date(), hour)
    return heatmap
