from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="citizen")  
    phone = Column(String, nullable=True)
    zone = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)



    reports = relationship("Report", back_populates="user")
    feedbacks = relationship("Feedback", back_populates="user")
    notifications = relationship("Notification", back_populates="user")

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    location = Column(String)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    status = Column(String, default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="reports")
    feedbacks = relationship("Feedback", back_populates="report")

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer)
    comments = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    report_id = Column(Integer, ForeignKey("reports.id"))

    user = relationship("User", back_populates="feedbacks")
    report = relationship("Report", back_populates="feedbacks")

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String)
    is_read = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="notifications")
