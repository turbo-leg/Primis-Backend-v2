from sqlalchemy.orm import Session
from app.models.user import User, Profile
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email, 
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create associated profile
    db_profile = Profile(
        user_id=db_user.id,
        first_name=user.first_name,
        last_name=user.last_name
    )
    db.add(db_profile)
    db.commit()
    
    return db_user
