from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, crud, schemas
from ai.classifier import classify_issue  

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SmartServe API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "SmartServe Backend Running"}


@app.post("/api/reports", response_model=schemas.ReportResponse)
def create_report(report: schemas.ReportCreate, db: Session = Depends(get_db)):
    return crud.create_report(db=db, report=report)

@app.get("/api/reports", response_model=list[schemas.ReportResponse])
def get_reports(db: Session = Depends(get_db)):
    return crud.get_reports(db)


@app.put("/api/reports/{report_id}")
def update_report(report_id: int, status: str, db: Session = Depends(get_db)):
  
    updated = crud.update_report_status(db, report_id, status)
    if not updated:
        raise HTTPException(status_code=404, detail="Report not found")
    return updated

@app.post("/api/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.get("/api/users", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


@app.post("/api/feedback", response_model=schemas.FeedbackResponse)
def create_feedback(feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    return crud.create_feedback(db, feedback)

@app.get("/api/feedback", response_model=list[schemas.FeedbackResponse])
def get_feedback(db: Session = Depends(get_db)):
    return crud.get_feedback(db)
