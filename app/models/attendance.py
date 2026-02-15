import enum
from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class AttendanceStatus(str, enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    EXCUSED = "excused"

from sqlalchemy import UniqueConstraint

class Attendance(Base):
    __tablename__ = "attendances"
    __table_args__ = (
        UniqueConstraint('session_id', 'student_id', name='uq_attendance_session_student'),
    )


    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("class_sessions.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(AttendanceStatus), default=AttendanceStatus.ABSENT, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    session = relationship("ClassSession", backref="attendances")
    student = relationship("User", backref="attendance_records")
