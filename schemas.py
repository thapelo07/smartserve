# schemas.py
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

# Pydantic v2-friendly model config:
# `model_config = {"from_attributes": True}` lets Pydantic read SQLAlchemy models.
# If your environment still uses pydantic v1, orm_mode will still work but may warn.
class UserBase(BaseModel):
    name: str = Field(..., min_length=2)
    email: str = Field(..., min_length=5)
    phone: Optional[str] = None
    zone: Optional[str] = None

    model_config = {"from_attributes": True}

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    role: Optional[str] = "citizen"

class UserResponse(UserBase):
    id: int
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}

class LoginRequest(BaseModel):
    email: str
    password: str

class ReportBase(BaseModel):
    description: str = Field(..., min_length=3)
    location: str = Field(..., min_length=2)

    model_config = {"from_attributes": True}

class ReportCreate(ReportBase):
    user_id: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    # When frontend sends multipart/form-data, use these form names

class ReportResponse(ReportBase):
    id: int
    latitude: float
    longitude: float
    status: str
    issue_type: Optional[str] = None
    image_url: Optional[str] = None
    user_id: Optional[int] = None
    created_at: datetime

    model_config = {"from_attributes": True}

class FeedbackCreate(BaseModel):
    user_id: Optional[int] = None
    message: str = Field(..., min_length=3)

    model_config = {"from_attributes": True}

class FeedbackResponse(FeedbackCreate):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}

class NotificationCreate(BaseModel):
    user_id: int
    message: str = Field(..., min_length=1)

    model_config = {"from_attributes": True}

class NotificationResponse(NotificationCreate):
    id: int
    created_at: datetime
    read: Optional[str] = None

    model_config = {"from_attributes": True}

class OTPCreate(BaseModel):
    email: str
    code: str

    model_config = {"from_attributes": True}

class OTPResponse(OTPCreate):
    id: int
    expires_at: datetime
    is_used: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}
