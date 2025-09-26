from datetime import datetime
from typing import Optional
from enum import Enum
from sqlmodel import SQLModel, Field

class UserRole(str, Enum):
    user = "user"
    creator = "creator"
    admin = "admin"

class CreatorApplicationStatus(str, Enum):
    none = "none"
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class UserStatus(str, Enum):
    active = "active"
    suspended = "suspended"
    blocked = "blocked"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    username: str = Field(index=True, nullable=False, unique=True)
    email: str = Field(index=True, nullable=False, unique=True)
    name: str = Field(nullable=False)
    country: str = Field(nullable=False)
    gender: str = Field(nullable=False)
    phone: Optional[str] = None
    password: str = Field(nullable=False)
    profile_photo_url: Optional[str] = None
    role: UserRole = Field(default=UserRole.user, nullable=False)
    creator_application_status: CreatorApplicationStatus = Field(default=CreatorApplicationStatus.none, nullable=False)
    status: UserStatus = Field(default=UserStatus.active, nullable=False)
    email_verified: bool = Field(default=False, nullable=False)
    last_login: Optional[datetime] = None
    otp_code: Optional[str] = None
    otp_expiry: Optional[datetime] = None
    reset_otp: str = Field(default=None, nullable=True)
    reset_otp_expiry: datetime = Field(default=None, nullable=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)