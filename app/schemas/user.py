from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    INSTRUCTOR = "instructor"
    STUDENT = "student"
    PARENT = "parent"

class UserBase(BaseModel):
    email: EmailStr

class ProfileBase(BaseModel):
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    phone_number: Optional[str] = None
    parent_email: Optional[EmailStr] = None

class Profile(ProfileBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    password: str = Field(min_length=8)
    role: UserRole = UserRole.STUDENT
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        import re
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).+$", v):
            raise ValueError("Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character")
        return v

class UserLogin(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    role: str
    language_pref: str
    profile: Optional[Profile] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
