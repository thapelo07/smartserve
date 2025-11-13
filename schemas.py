from pydantic import BaseModel
from datetime import datetime

# ✅ REPORT SCHEMAS
class ReportBase(BaseModel):
    description: str
    location: str | None = None
    latitude: float = 0.0
    longitude: float = 0.0

class ReportCreate(ReportBase):
    description: str
    location: str
    user_id: int | None = None# 🔗 Connect the report to a user

class ReportResponse(ReportBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# USER
class UserBase(BaseModel):
    name: str
    email: str
    role: str = "citizen"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    phone: str | None = None
    zone: str | None = None
    created_at: datetime
    class Config:
        from_attributes = True

# FEEDBACK
class FeedbackBase(BaseModel):
    rating: int
    comments: str | None = None

class FeedbackCreate(FeedbackBase):
    report_id: int
    user_id: int

class FeedbackResponse(FeedbackBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

# NOTIFICATION
class NotificationBase(BaseModel):
    message: str
    user_id: int

class NotificationResponse(NotificationBase):
    id: int
    is_read: int
    created_at: datetime
    class Config:
        from_attributes = True
