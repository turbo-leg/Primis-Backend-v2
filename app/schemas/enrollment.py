from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.enrollment import EnrollmentStatus, PaymentStatus

class EnrollmentBase(BaseModel):
    course_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentUpdate(BaseModel):
    status: Optional[EnrollmentStatus] = None
    payment_status: Optional[PaymentStatus] = None

class EnrollmentResponse(EnrollmentBase):
    id: int
    user_id: int
    enrollment_date: datetime
    status: EnrollmentStatus
    payment_status: PaymentStatus

    model_config = ConfigDict(from_attributes=True)
