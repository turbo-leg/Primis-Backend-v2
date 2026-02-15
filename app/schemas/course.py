from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class CourseBase(BaseModel):
    title_en: str
    title_mn: str
    description_en: Optional[str] = None
    description_mn: Optional[str] = None
    price: float = 0.0
    is_published: bool = False

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    title_en: Optional[str] = None
    title_mn: Optional[str] = None

class CourseResponse(CourseBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
