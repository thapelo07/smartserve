# ai_model/train_model.py

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sqlalchemy.orm import Session
import os
import sys

# allow backend imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database import SessionLocal
import models

MODEL_PATH = "ai_model/model.pkl"
VECTORIZER_PATH = "ai_model/vectorizer.pkl"


def train_model():
    db: Session = SessionLocal()

    # Fetch all reports that have both description & issue_type
    reports = db.query(models.Report).filter(models.Report.issue_type.isnot(None)).all()

    if not reports or len(reports) < 5:
        print("❌ Not enough labeled data to train model.")
        return None

    descriptions = [r.description for r in reports]
    labels = [r.issue_type for r in reports]

    # NLP pipeline
    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(descriptions)

    model = MultinomialNB()
    model.fit(X, labels)

    # Save
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)

    print("✅ Model trained and saved!")
    return model


if __name__ == "__main__":
    train_model()
