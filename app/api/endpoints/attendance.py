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
    # For now, allow any active user for simplicity, but strictly Instructor should check
    return crud_attendance.create_or_update_attendance(db, attendance_in)

@router.get("/session/{session_id}", response_model=List[AttendanceResponse])
def read_session_attendance(
    session_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    return crud_attendance.get_session_attendance(db, session_id, skip, limit)

@router.get("/student/{student_id}", response_model=List[AttendanceResponse])
def read_student_attendance(
    student_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    return crud_attendance.get_student_attendance(db, student_id, skip, limit)
