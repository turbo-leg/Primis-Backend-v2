import enum
from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class EnrollmentStatus(str, enum.Enum):
    ACTIVE = "active"
    DROPPED = "dropped"
    COMPLETED = "completed"

class PaymentStatus(str, enum.Enum):
    UNPAID = "unpaid"
    PAID = "paid"
    WAIVED = "waived"

class Enrollment(Base):
    __tablename__ = "enrollments"
    __table_args__ = (
        UniqueConstraint('user_id', 'course_id', name='uq_enrollment_user_course'),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    enrollment_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(EnrollmentStatus), default=EnrollmentStatus.ACTIVE, nullable=False)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.UNPAID, nullable=False)

    user = relationship("User", backref="enrollments")
    course = relationship("Course", backref="enrollments")
