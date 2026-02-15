from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.crud import crud_attendance
from app.schemas.attendance import AttendanceCreate, AttendanceResponse, AttendanceUpdate
from app.models.user import User
from app.models.attendance import AttendanceStatus

router = APIRouter()

@router.post("/", response_model=AttendanceResponse)
def mark_attendance(
    attendance_in: AttendanceCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    # Check permissions (Instructor of the session or Admin)
    if not _user_can_mark_attendance(current_user):
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions to mark attendance",
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
    # Instructor or Admin can view session attendance
    if not _user_can_mark_attendance(current_user):
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
    if current_user.id != student_id and not _user_can_mark_attendance(current_user):
        raise HTTPException(status_code=403, detail="Not authorized to view this student's attendance")
    return crud_attendance.get_student_attendance(db, student_id, skip, limit)

def _user_can_mark_attendance(user: User) -> bool:
    if user.role in ["admin", "instructor"]:
        return True
    return False
