import models, schemas
from sqlalchemy.orm import Session
from fastapi import HTTPException
from utils.geocode import get_coordinates
from datetime import datetime, timedelta
from models import OTP

# USERS
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


# REPORTS
def create_report(db: Session, report: schemas.ReportCreate):
    lat, lon = get_coordinates(report.location)
    if not lat or not lon:
        raise HTTPException(status_code=400, detail="Invalid location")
    
    new_report = models.Report(
        description=report.description,
        location=report.location,
        latitude=lat,
        longitude=lon,
        user_id=report.user_id if report.user_id else None,
        status="Pending"
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    print(f"✅ Saved report with coordinates: ({lat}, {lon})")
    return new_report


def get_reports(db: Session):
    return db.query(models.Report).all()


# FEEDBACK
def create_feedback(db: Session, feedback: schemas.FeedbackCreate):
    db_feedback = models.Feedback(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback


def get_feedback(db: Session):
    return db.query(models.Feedback).all()


# NOTIFICATIONS
def create_notification(db: Session, message: str, user_id: int):
    db_notification = models.Notification(message=message, user_id=user_id)
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification



def create_otp(db: Session, email: str, otp_code: str):
    expires_at = datetime.utcnow() + timedelta(minutes=5)
    otp_entry = OTP(email=email, code=otp_code, expires_at=expires_at)
    db.add(otp_entry)
    db.commit()
    db.refresh(otp_entry)
    return otp_entry

def verify_otp(db: Session, email: str, otp_code: str):
    otp_entry = (
        db.query(OTP)
        .filter(OTP.email == email, OTP.code == otp_code, OTP.is_used == False)
        .first()
    )
    if not otp_entry:
        return False

    if otp_entry.expires_at < datetime.utcnow():
        return False

    otp_entry.is_used = True
    db.commit()
    return True


# ✅ Update report details (PATCH)
def update_report_partial(db: Session, report_id: int, update_data: dict):
    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    for key, value in update_data.items():
        if hasattr(report, key) and value is not None:
            setattr(report, key, value)

    db.commit()
    db.refresh(report)
    return report


# ✅ Delete a report (DELETE)
def delete_report(db: Session, report_id: int):
    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    db.delete(report)
    db.commit()
    return {"message": f"Report {report_id} deleted successfully"}

def patch_report(db: Session, report_id: int, updates: dict):
    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    # Loop through only the fields that were passed in the PATCH request
    for key, value in updates.items():
        if hasattr(report, key):
            setattr(report, key, value)

    db.commit()
    db.refresh(report)
    return report

