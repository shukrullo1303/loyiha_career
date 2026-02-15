"""
Ходимлар API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.employee import Employee
from app.schemas.employee import (
    Employee as EmployeeSchema,
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeFaceCreate
)
from app.services.face_recognition_service import FaceRecognitionService

router = APIRouter()
face_service = FaceRecognitionService()


@router.get("/", response_model=List[EmployeeSchema])
async def get_employees(
    location_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Ходимлар рўйхати"""
    employees = db.query(Employee).filter(
        Employee.location_id == location_id
    ).offset(skip).limit(limit).all()
    
    return employees


@router.post("/", response_model=EmployeeSchema)
async def create_employee(
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Ходим яратиш"""
    employee = Employee(**employee_data.dict())
    
    db.add(employee)
    db.commit()
    db.refresh(employee)
    
    return employee


@router.post("/{employee_id}/face")
async def add_employee_face(
    employee_id: int,
    face_data: EmployeeFaceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Ходим юзини қўшиш"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ходим топилмади"
        )
    
    result = await face_service.add_employee_face(
        employee_id,
        face_data.image_base64
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Хатолик")
        )
    
    return result


@router.get("/{employee_id}", response_model=EmployeeSchema)
async def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Ходим маълумотлари"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ходим топилмади"
        )
    
    return employee


@router.put("/{employee_id}", response_model=EmployeeSchema)
async def update_employee(
    employee_id: int,
    employee_data: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Ходимни янгилаш"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ходим топилмади"
        )
    
    update_data = employee_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(employee, field, value)
    
    db.commit()
    db.refresh(employee)
    
    return employee
