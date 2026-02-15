from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class ClassSessionBase(BaseModel):
    course_id: int
    instructor_id: int
    name: Optional[str] = None
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None

class ClassSessionCreate(ClassSessionBase):
    pass

class ClassSessionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    instructor_id: Optional[int] = None

class ClassSessionResponse(ClassSessionBase):
    id: int

    class Config:
        from_attributes = True
