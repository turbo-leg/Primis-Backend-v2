from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.crud import crud_class_session
from app.schemas.class_session import ClassSessionCreate, ClassSessionUpdate, ClassSessionResponse
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[ClassSessionResponse])
def read_sessions(
    skip: int = 0, 
    limit: int = 100, 
    course_id: Optional[int] = None,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    sessions = crud_class_session.get_class_sessions(db, skip=skip, limit=limit, course_id=course_id)
    return sessions

@router.post("/", response_model=ClassSessionResponse)
def create_session(
    session: ClassSessionCreate, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    return crud_class_session.create_class_session(db=db, session=session)

@router.get("/{session_id}", response_model=ClassSessionResponse)
def read_session(
    session_id: int, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    session = crud_class_session.get_class_session(db, session_id=session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.put("/{session_id}", response_model=ClassSessionResponse)
def update_session(
    session_id: int,
    session_in: ClassSessionUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    session = crud_class_session.update_class_session(db, session_id=session_id, session_in=session_in)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.delete("/{session_id}", response_model=ClassSessionResponse)
def delete_session(
    session_id: int, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    session = crud_class_session.delete_class_session(db, session_id=session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session
