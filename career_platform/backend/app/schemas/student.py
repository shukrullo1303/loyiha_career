from typing import Optional

from pydantic import BaseModel


class StudentBase(BaseModel):
    id: int
    fio: Optional[str] = None
    birth_year: Optional[int] = None
    gender: Optional[str] = None
    region: Optional[str] = None
    school: Optional[str] = None
    class_level: Optional[str] = None

    class Config:
        orm_mode = True


class StudentCreate(BaseModel):
    fio: str
    birth_year: Optional[int] = None
    gender: Optional[str] = None
    region: Optional[str] = None
    school: Optional[str] = None
    class_level: Optional[str] = None

