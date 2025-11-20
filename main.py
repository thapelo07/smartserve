from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import logging
from sqlalchemy import func
from fastapi import UploadFile, File, Form
import shutil
import os
from ai_model.analytics import predict_issue, predict_next_issue, forecast_next_issue_global
import models, schemas, crud
from database import engine, SessionLocal

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SmartServe API", version="2.0")

# --------------------------------------------------------
# GLOBAL CORS
# --------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

# --------------------------------------------------------
# GLOBAL ERROR HANDLER
# --------------------------------------------------------
@app.middleware("http")
async def error_logger(request, call_next):
    try:
        return await call_next(request)

    except Exception as e:
        logging.error(f"🔥 INTERNAL ERROR: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": "Server failed internally. Try again later."}
        )

# --------------------------------------------------------
# DB Dependency
# --------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------------------------------------------------------
# ROOT
# --------------------------------------------------------
@app.get("/")
def home():
    return {"message": "SmartServe Backend Running"}

# --------------------------------------------------------
# USERS
# --------------------------------------------------------
@app.post("/api/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.get("/api/users", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/api/login")
def login_user(credentials: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    if not pwd_context.verify(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return {"message": "Login successful", "user_id": user.id}

# --------------------------------------------------------
# REPORTS
# --------------------------------------------------------
@app.post("/api/reports", response_model=schemas.ReportResponse)
def create_report(report: schemas.ReportCreate, db: Session = Depends(get_db)):
    return crud.create_report(db, report)

@app.get("/api/reports", response_model=list[schemas.ReportResponse])
def get_reports(db: Session = Depends(get_db)):
    return crud.get_reports(db)

@app.delete("/api/reports/{report_id}")
def delete_report(report_id: int, db: Session = Depends(get_db)):
    return crud.delete_report(db, report_id)

# ---------------------------
# ANALYTICS ROUTES
# ---------------------------
@app.get("/api/analytics/total")
def analytics_total(db: Session = Depends(get_db)):
    return {"total_reports": crud.get_total_reports(db)}

@app.get("/api/analytics/pending")
def analytics_pending(db: Session = Depends(get_db)):
    return {"pending_reports": crud.get_pending_reports(db)}

@app.get("/api/analytics/resolved")
def analytics_resolved(db: Session = Depends(get_db)):
    return {"resolved_reports": crud.get_resolved_reports(db)}

@app.get("/api/analytics/by-location")
def analytics_by_location(db: Session = Depends(get_db)):
    return {"locations": crud.get_reports_by_location(db)}

@app.patch("/api/reports/{report_id}")
def patch_report(report_id: int, updates: dict, db: Session = Depends(get_db)):
    return crud.patch_report(db, report_id, updates)

# --------------------------------------------------------
# FEEDBACK
# --------------------------------------------------------
@app.post("/api/feedback", response_model=schemas.FeedbackResponse)
def create_feedback(feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    return crud.create_feedback(db, feedback)

@app.get("/api/feedback", response_model=list[schemas.FeedbackResponse])
def get_feedback(db: Session = Depends(get_db)):
    return crud.get_feedback(db)

# --------------------------------------------------------
# NOTIFICATIONS
# --------------------------------------------------------
@app.post("/api/notifications/{user_id}")
def send_notification(user_id: int, message: str, db: Session = Depends(get_db)):
    return crud.create_notification(db, message, user_id)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/api/reports/upload-image")
async def upload_report_image(
    report_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Ensure it's an image
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files allowed")

    # Create file path
    ext = file.filename.split(".")[-1].lower()
    file_path = f"{UPLOAD_DIR}/report_{report_id}.{ext}"

    # Save file to disk
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 🔗 Update DB record
    updated_report = crud.attach_image(db, report_id, file_path)

    return {
        "message": "Image uploaded and attached",
        "file_path": file_path,
        "report": updated_report
    }


@app.post("/api/ai/predict")
def ai_predict(payload: dict):
    return predict_issue(payload["text"])

@app.get("/api/ai/predict-location")
def ai_predict_location(loc: str):
    return predict_next_issue(loc)

@app.get("/api/ai/predict-global")
def ai_predict_global():
    return forecast_next_issue_global()
