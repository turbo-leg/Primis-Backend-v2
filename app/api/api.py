from fastapi import APIRouter
from app.api.endpoints import auth, courses, class_sessions


api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
api_router.include_router(class_sessions.router, prefix="/classes", tags=["classes"])


