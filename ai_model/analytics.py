# ai_model/analytics.py

import joblib
import os
import sys
from sqlalchemy.orm import Session
from collections import Counter

# allow backend imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from database import SessionLocal
import models

MODEL_PATH = "ai_model/model.pkl"
VECTORIZER_PATH = "ai_model/vectorizer.pkl"


# -------------------------------------------
# 🔮 Predict issue type (NLP classification)
# -------------------------------------------
def predict_issue(text: str):
    if not os.path.exists(MODEL_PATH):
        return {"error": "Model not trained"}

    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)

    X = vectorizer.transform([text])
    prediction = model.predict(X)[0]

    return {"predicted_issue_type": prediction}


# -------------------------------------------------
# 📈 Predict the most common issue in a location
# -------------------------------------------------
def predict_next_issue(location: str):
    db: Session = SessionLocal()

    reports = (
        db.query(models.Report)
        .filter(models.Report.location.ilike(f"%{location}%"))
        .all()
    )

    if not reports:
        return {"location": location, "prediction": "No historical data"}

    types = [r.issue_type for r in reports if r.issue_type]

    if not types:
        return {"location": location, "prediction": "No labeled types yet"}

    most_common = Counter(types).most_common(1)[0][0]
    return {"location": location, "prediction": most_common}


# -------------------------------------------------
# 📊 Overall predictive analytics (simple forecast)
# -------------------------------------------------
def forecast_next_issue_global():
    db: Session = SessionLocal()
    reports = db.query(models.Report).all()

    types = [r.issue_type for r in reports if r.issue_type]

    if not types:
        return {"prediction": "No data available"}

    counter = Counter(types)
    most_common = counter.most_common(1)[0]
    total = sum(counter.values())

    probability = round((most_common[1] / total) * 100, 2)

    return {
        "next_probable_issue": most_common[0],
        "probability": f"{probability}%"
    }
