from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.crud import crud_course
from app.schemas.course import CourseCreate, CourseResponse
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[CourseResponse])
def read_courses(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    courses = crud_course.get_courses(db, skip=skip, limit=limit)
    return courses

@router.post("/", response_model=CourseResponse)
def create_course(
    course: CourseCreate, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    # In a real app, check if user is instructor/admin
    return crud_course.create_course(db=db, course=course)

@router.get("/{course_id}", response_model=CourseResponse)
def read_course(
    course_id: int, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    course = crud_course.get_course(db, course_id=course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.delete("/{course_id}", response_model=CourseResponse)
def delete_course(
    course_id: int, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    course = crud_course.delete_course(db, course_id=course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course
