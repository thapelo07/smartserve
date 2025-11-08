import models, schemas
from sqlalchemy.orm import Session
from fastapi import HTTPException


def create_user(db: Session, user: schemas.UserCreate):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_users(db: Session):
    return db.query(models.User).all()

def create_report(db: Session, report: schemas.ReportCreate):
    new_report = models.Report(
        description=report.description,
        location=report.location,
        latitude=report.latitude,
        longitude=report.longitude,
        user_id=report.user_id if report.user_id else None, 
        status="Pending"
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report

def create_feedback(db: Session, feedback: schemas.FeedbackCreate):
    db_feedback = models.Feedback(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def get_feedback(db: Session):
    return db.query(models.Feedback).all()

def create_notification(db: Session, message: str, user_id: int):
    db_notification = models.Notification(message=message, user_id=user_id)
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification
