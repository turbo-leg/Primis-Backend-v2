from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api import deps
from app.core import security
from app.core.config import settings
from app.crud import crud_user
from app.schemas.user import UserCreate, UserResponse, Token
from app.models.user import User

router = APIRouter()

@router.post("/login", response_model=Token)
def login_access_token(db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud_user.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(user.id, expires_delta=access_token_expires)
    
    # Subject should be email as per deps.py logic (sub=email)
    access_token = security.create_access_token(user.email, expires_delta=access_token_expires)
    
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }

@router.post("/register", response_model=UserResponse)
def register_user(user_in: UserCreate, db: Session = Depends(deps.get_db)):
    user = crud_user.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user = crud_user.create_user(db, user=user_in)
    return user

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(deps.get_current_active_user)):
    return current_user
