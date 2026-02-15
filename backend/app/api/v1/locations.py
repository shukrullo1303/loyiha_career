"""
Локациялар API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.location import Location
from app.schemas.location import Location as LocationSchema, LocationCreate, LocationUpdate

router = APIRouter()


@router.get("/", response_model=List[LocationSchema])
async def get_locations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Локациялар рўйхати"""
    locations = db.query(Location).offset(skip).limit(limit).all()
    return locations


@router.post("/", response_model=LocationSchema)
async def create_location(
    location_data: LocationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Локация яратиш"""
    location = Location(
        **location_data.dict(),
        owner_id=current_user.id
    )
    
    db.add(location)
    db.commit()
    db.refresh(location)
    
    return location


@router.get("/{location_id}", response_model=LocationSchema)
async def get_location(
    location_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Локация маълумотлари"""
    location = db.query(Location).filter(Location.id == location_id).first()
    
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Локация топилмади"
        )
    
    return location


@router.put("/{location_id}", response_model=LocationSchema)
async def update_location(
    location_id: int,
    location_data: LocationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Локацияни янгилаш"""
    location = db.query(Location).filter(Location.id == location_id).first()
    
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Локация топилмади"
        )
    
    # Фақат эга янгилай олади
    if location.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Рухсат йўқ"
        )
    
    # Янгилаш
    update_data = location_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(location, field, value)
    
    db.commit()
    db.refresh(location)
    
    return location


@router.delete("/{location_id}")
async def delete_location(
    location_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Локацияни ўчириш"""
    location = db.query(Location).filter(Location.id == location_id).first()
    
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Локация топилмади"
        )
    
    # Фақат админ ёки эга ўчира олади
    if location.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Рухсат йўқ"
        )
    
    db.delete(location)
    db.commit()
    
    return {"message": "Локация ўчирилди"}
