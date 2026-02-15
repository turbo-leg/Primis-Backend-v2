from sqlalchemy.orm import Session
from app.models.class_session import ClassSession
from app.schemas.class_session import ClassSessionCreate, ClassSessionUpdate

def get_class_session(db: Session, session_id: int):
    return db.query(ClassSession).filter(ClassSession.id == session_id).first()

def get_class_sessions(db: Session, skip: int = 0, limit: int = 100, course_id: int = None):
    query = db.query(ClassSession)
    if course_id:
        query = query.filter(ClassSession.course_id == course_id)
    return query.offset(skip).limit(limit).all()

def create_class_session(db: Session, session: ClassSessionCreate):
    db_session = ClassSession(**session.model_dump())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def update_class_session(db: Session, session_id: int, session_in: ClassSessionUpdate):
    db_session = get_class_session(db, session_id)
    if not db_session:
        return None
    
    update_data = session_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_session, key, value)

    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def delete_class_session(db: Session, session_id: int):
    db_session = get_class_session(db, session_id)
    if db_session:
        db.delete(db_session)
        db.commit()
    return db_session
