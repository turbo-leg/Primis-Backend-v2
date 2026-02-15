from sqlalchemy.orm import Session
from app.models.attendance import Attendance, AttendanceStatus
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate

def get_attendance(db: Session, session_id: int, student_id: int):
    return db.query(Attendance).filter(
        Attendance.session_id == session_id,
        Attendance.student_id == student_id
    ).first()

def create_or_update_attendance(db: Session, attendance_in: AttendanceCreate):
    db_attendance = get_attendance(db, attendance_in.session_id, attendance_in.student_id)
    if db_attendance:
        db_attendance.status = attendance_in.status
        # db_attendance.timestamp = func.now() # Auto updated if using onupdate? No, timestamp is creation time usually.
    else:
        db_attendance = Attendance(**attendance_in.model_dump())
        db.add(db_attendance)
    
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

def get_session_attendance(db: Session, session_id: int, skip: int = 0, limit: int = 100):
    return db.query(Attendance).filter(Attendance.session_id == session_id).offset(skip).limit(limit).all()

def get_student_attendance(db: Session, student_id: int, skip: int = 0, limit: int = 100):
    return db.query(Attendance).filter(Attendance.student_id == student_id).offset(skip).limit(limit).all()
