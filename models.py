from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import func

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)  # hashed password
    role = Column(String(50), default="citizen")  # e.g., citizen, supervisor, admin
    phone = Column(String(50), nullable=True)
    zone = Column(String(100), nullable=True)  # optional zone/area assignment
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    reports = relationship("Report", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    location = Column(String(255), nullable=False)  # human readable e.g. "Tembisa CBD"
    latitude = Column(Float, nullable=False, default=0.0)
    longitude = Column(Float, nullable=False, default=0.0)
    status = Column(String(50), default="Pending", nullable=False)  # Pending, InProgress, Resolved
    issue_type = Column(String(120), nullable=True)  # e.g., "Pothole", "Water Leak", "Power Outage"
    image_url = Column(String(512), nullable=True)  # served from /uploads/...
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    
    user = relationship("User", back_populates="reports")
    image_path = Column(String, nullable=True)
class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Optionally relate feedback to user
    user = relationship("User", backref="feedbacks")

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(String(512), nullable=False)
    read = Column(String(10), default="false")  # or use Boolean with SQLite quirks in mind
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="notifications")

class OTP(Base):
    __tablename__ = "otps"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), index=True, nullable=False)
    code = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_used = Column(String(10), default="false")  # "true" / "false" or change to Boolean if preferred
