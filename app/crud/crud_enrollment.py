from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.enrollment import Enrollment, EnrollmentStatus, PaymentStatus
from app.schemas.enrollment import EnrollmentCreate, EnrollmentUpdate

def get_enrollment(db: Session, enrollment_id: int) -> Optional[Enrollment]:
    return db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()

def get_enrollments_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Enrollment]:
    return db.query(Enrollment).filter(Enrollment.user_id == user_id).offset(skip).limit(limit).all()

def get_enrollment_by_user_and_course(db: Session, user_id: int, course_id: int) -> Optional[Enrollment]:
    return db.query(Enrollment).filter(Enrollment.user_id == user_id, Enrollment.course_id == course_id).first()

def create_enrollment(db: Session, obj_in: EnrollmentCreate, user_id: int) -> Enrollment:
    db_obj = Enrollment(
        user_id=user_id,
        course_id=obj_in.course_id,
        status=EnrollmentStatus.ACTIVE,
        payment_status=PaymentStatus.UNPAID
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_enrollment(db: Session, db_obj: Enrollment, obj_in: EnrollmentUpdate) -> Enrollment:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
