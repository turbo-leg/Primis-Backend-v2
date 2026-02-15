from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from app.models.attendance import AttendanceStatus

class AttendanceBase(BaseModel):
    session_id: int
    student_id: int
    status: AttendanceStatus

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceUpdate(BaseModel):
    status: AttendanceStatus

class AttendanceResponse(AttendanceBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class AttendanceList(BaseModel):
    items: List[AttendanceResponse]
