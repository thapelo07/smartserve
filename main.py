from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, crud, schemas
from ai.classifier import classify_issue  # we’ll use this later for AI
from utils.otp import generate_otp, send_otp_email


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SmartServe API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "SmartServe Backend Running"}

# ✅ Create new report
@app.post("/api/reports", response_model=schemas.ReportResponse)
def create_report(report: schemas.ReportCreate, db: Session = Depends(get_db)):
    return crud.create_report(db=db, report=report)

# ✅ Get all reports
@app.get("/api/reports", response_model=list[schemas.ReportResponse])
def get_reports(db: Session = Depends(get_db)):
    return crud.get_reports(db)

# ✅ 🆕 Update report status (add this section here)
@app.put("/api/reports/{report_id}")
def update_report(report_id: int, status: str, db: Session = Depends(get_db)):
    """
    Update a report's status by its ID.
    Example: /api/reports/1?status=Resolved
    """
    updated = crud.update_report_status(db, report_id, status)
    if not updated:
        raise HTTPException(status_code=404, detail="Report not found")
    return updated

# 🗑️ DELETE a report
@app.delete("/api/reports/{report_id}")
def delete_report(report_id: int, db: Session = Depends(get_db)):
    return crud.delete_report(db, report_id)


# 🩹 PATCH (partial update) a report
@app.patch("/api/reports/{report_id}")
def patch_report(report_id: int, updates: dict, db: Session = Depends(get_db)):
    """
    Example JSON body:
    {
      "status": "Resolved",
      "description": "Technicians fixed the issue"
    }
    """
    return crud.patch_report(db, report_id, updates)


# USERS
@app.post("/api/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.get("/api/users", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


@app.post("/api/send_otp")
def send_otp(email: str, db: Session = Depends(get_db)):
    otp_code = generate_otp()
    crud.create_otp(db, email=email, otp_code=otp_code)
    send_otp_email(email, otp_code)
    return {"message": f"OTP sent to {email}"}


@app.post("/api/verify_otp")
def verify_otp(email: str, otp: str, db: Session = Depends(get_db)):
    is_valid = crud.verify_otp(db, email=email, otp_code=otp)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    return {"message": "OTP verified successfully"}

# FEEDBACK
@app.post("/api/feedback", response_model=schemas.FeedbackResponse)
def create_feedback(feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    return crud.create_feedback(db, feedback)

@app.get("/api/feedback", response_model=list[schemas.FeedbackResponse])
def get_feedback(db: Session = Depends(get_db)):
    return crud.get_feedback(db)
