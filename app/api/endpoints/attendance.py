from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.crud import crud_attendance
from app.schemas.attendance import AttendanceCreate, AttendanceResponse, AttendanceUpdate
from app.schemas.user import UserRole
from app.models.user import User
from app.models.class_session import ClassSession
from app.models.attendance import AttendanceStatus

router = APIRouter()

@router.post("/", response_model=AttendanceResponse)
def mark_attendance(
    attendance_in: AttendanceCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    # Check permissions (Instructor of the session or Admin)
    # Check if session exists first
    session = db.query(ClassSession).filter(ClassSession.id == attendance_in.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Class session not found")
        
    if not _user_can_mark_attendance(current_user, session):
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions to mark attendance for this session",
        )
    return crud_attendance.create_or_update_attendance(db, attendance_in)

@router.get("/session/{session_id}", response_model=List[AttendanceResponse])
def read_session_attendance(
    session_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    session = db.query(ClassSession).filter(ClassSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Class session not found")

    # Instructor or Admin can view session attendance
    if not _user_can_mark_attendance(current_user, session):
         raise HTTPException(status_code=403, detail="Not authorized to view session attendance")
    return crud_attendance.get_session_attendance(db, session_id, skip, limit)

@router.get("/student/{student_id}", response_model=List[AttendanceResponse])
def read_student_attendance(
    student_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    # User can view their own, or Instructor/Admin can view
    # Note: instructors can view student attendance generally or only for their sessions? 
    # For now, keeping it simple: admins/instructors can view any student's attendance history
    if current_user.id != student_id and not _user_is_admin_or_instructor(current_user):
        raise HTTPException(status_code=403, detail="Not authorized to view this student's attendance")
    return crud_attendance.get_student_attendance(db, student_id, skip, limit)

def _user_is_admin_or_instructor(user: User) -> bool:
    # Use UserRole enum values
    if user.role in [UserRole.ADMIN.value, UserRole.INSTRUCTOR.value]:
        return True
    return False

def _user_can_mark_attendance(user: User, session: ClassSession) -> bool:
    if user.role == UserRole.ADMIN.value:
        return True
    if user.role == UserRole.INSTRUCTOR.value:
        # Check if they are the instructor for this session
        return session.instructor_id == user.id
    return False
