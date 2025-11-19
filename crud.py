from sqlalchemy.orm import Session
from fastapi import HTTPException
from utils.geocode import get_coordinates
from passlib.context import CryptContext

import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -----------------------------------
# USERS
# -----------------------------------
def create_user(db: Session, user: schemas.UserCreate):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_pw = pwd_context.hash(user.password)

    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_pw
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error when creating user")


def get_users(db: Session):
    try:
        return db.query(models.User).all()
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch users")


# -----------------------------------
# REPORTS (GIS + CRUD)
# -----------------------------------
def create_report(db: Session, report: schemas.ReportCreate):
    # Normalize user_id
    user_id = report.user_id if report.user_id not in (0, "0", "", None) else None

    # Geocode location with safety
    try:
        lat, lon = get_coordinates(report.location)
    except Exception:
        lat, lon = None, None

    if lat is None or lon is None:
        lat, lon = 0.0, 0.0

    new_report = models.Report(
        description=report.description,
        location=report.location,
        latitude=lat,
        longitude=lon,
        user_id=user_id,
        status="Pending"
    )

    try:
        db.add(new_report)
        db.commit()
        db.refresh(new_report)
        return new_report
    except Exception as e:
        db.rollback()
        print("🔥 DB ERROR:", e)
        raise HTTPException(status_code=500, detail="Failed to create report")


def get_reports(db: Session):
    try:
        return db.query(models.Report).all()
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch reports")


def delete_report(db: Session, report_id: int):
    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    try:
        db.delete(report)
        db.commit()
        return {"message": "Report deleted successfully"}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete report")


def patch_report(db: Session, report_id: int, updates: dict):
    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    try:
        for key, value in updates.items():
            if hasattr(report, key):
                setattr(report, key, value)
        db.commit()
        db.refresh(report)
        return report
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update report")


# -----------------------------------
# FEEDBACK
# -----------------------------------
def create_feedback(db: Session, feedback: schemas.FeedbackCreate):
    try:
        db_feedback = models.Feedback(**feedback.dict())
        db.add(db_feedback)
        db.commit()
        db.refresh(db_feedback)
        return db_feedback
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to submit feedback")


def get_feedback(db: Session):
    try:
        return db.query(models.Feedback).all()
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch feedback")


# -----------------------------------
# NOTIFICATIONS
# -----------------------------------
def create_notification(db: Session, message: str, user_id: int):
    try:
        notification = models.Notification(message=message, user_id=user_id)
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create notification")


# -----------------------------------
# ANALYTICS
# -----------------------------------
def get_total_reports(db: Session):
    return db.query(models.Report).count()


def get_pending_reports(db: Session):
    return db.query(models.Report).filter(models.Report.status == "Pending").count()


def get_resolved_reports(db: Session):
    return db.query(models.Report).filter(models.Report.status == "Resolved").count()


def get_reports_by_location(db: Session):
    results = (
        db.query(models.Report.location, models.func.count(models.Report.id))
        .group_by(models.Report.location)
        .all()
    )
    return [{"location": loc, "count": count} for loc, count in results]


# -----------------------------------
# IMAGE ATTACH
# -----------------------------------
def attach_image(db: Session, report_id: int, file_path: str):
    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    report.image_path = file_path

    try:
        db.commit()
        db.refresh(report)
        return report
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to attach image")
