from fastapi import APIRouter
from app.api.endpoints import auth, courses, class_sessions, attendance, enrollments


api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
api_router.include_router(class_sessions.router, prefix="/classes", tags=["classes"])
api_router.include_router(attendance.router, prefix="/attendance", tags=["attendance"])
api_router.include_router(enrollments.router, prefix="/enrollments", tags=["enrollments"])
