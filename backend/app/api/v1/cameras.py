"""
Камералар API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.location import Camera
from app.services.camera_service import CameraService
from app.services.video_analytics_service import VideoAnalyticsService

router = APIRouter()
camera_service = CameraService()
video_service = VideoAnalyticsService()


@router.get("/")
async def list_cameras(
    location_id: Optional[int] = None,
    current_user: User = Depends(get_current_user)
):
    """Камералар рўйхати"""
    cameras = await camera_service.list_cameras(location_id)
    return cameras


@router.get("/{camera_id}/status")
async def get_camera_status(
    camera_id: int,
    current_user: User = Depends(get_current_user)
):
    """Камера статуси"""
    status = await camera_service.get_camera_status(camera_id)
    return status


@router.post("/{camera_id}/analyze")
async def analyze_camera_stream(
    camera_id: int,
    duration: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Камера оқимини таҳлил қилиш"""
    camera = db.query(Camera).filter(Camera.id == camera_id).first()
    
    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Камера топилмади"
        )
    
    if not camera.stream_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Камера оқим URL мавжуд эмас"
        )
    
    result = await video_service.process_camera_stream(
        camera.location_id,
        camera_id,
        camera.stream_url,
        duration
    )
    
    return result


@router.post("/connect")
async def connect_camera(
    ip_address: str,
    port: int = 80,
    username: Optional[str] = None,
    password: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Камерага уланиш"""
    result = await camera_service.connect_camera(
        ip_address,
        port,
        username,
        password
    )
    return result
