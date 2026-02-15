"""
Интеграция API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.integration_service import IntegrationService

router = APIRouter()
integration_service = IntegrationService()


@router.post("/tax/sync/{location_id}")
async def sync_tax_data(
    location_id: int,
    tax_id: str,
    current_user: User = Depends(get_current_user)
):
    """Солиқ маълумотларини синхронлаш"""
    result = await integration_service.sync_tax_data(location_id, tax_id)
    return result


@router.post("/kkt/sync/{location_id}")
async def sync_kkt_data(
    location_id: int,
    kkt_serial: str,
    current_user: User = Depends(get_current_user)
):
    """ККТ маълумотларини синхронлаш"""
    result = await integration_service.sync_kkt_data(location_id, kkt_serial)
    return result
