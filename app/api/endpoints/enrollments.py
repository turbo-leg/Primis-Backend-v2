from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User
from app.models.enrollment import Enrollment
from app.schemas.enrollment import EnrollmentCreate, EnrollmentResponse, EnrollmentUpdate
from app.crud import crud_enrollment

router = APIRouter()

@router.post("/", response_model=EnrollmentResponse)
def create_enrollment(
    *,
    db: Session = Depends(deps.get_db),
    enrollment_in: EnrollmentCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Enroll current user in a course.
    """
    # Check if already enrolled
    existing = crud_enrollment.get_enrollment_by_user_and_course(
        db, user_id=current_user.id, course_id=enrollment_in.course_id
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail="User already enrolled in this course"
        )
    
    enrollment = crud_enrollment.create_enrollment(db, obj_in=enrollment_in, user_id=current_user.id)
    return enrollment

@router.get("/me", response_model=List[EnrollmentResponse])
def read_my_enrollments(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user's enrollments.
    """
    return crud_enrollment.get_enrollments_by_user(db, user_id=current_user.id, skip=skip, limit=limit)

@router.get("/{enrollment_id}", response_model=EnrollmentResponse)
def read_enrollment(
    enrollment_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a specific enrollment by ID.
    """
    enrollment = crud_enrollment.get_enrollment(db, enrollment_id=enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    if enrollment.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return enrollment
