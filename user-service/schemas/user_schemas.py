from typing import Optional, Annotated
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

# Enums (keep consistent with your SQLModel)
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



class UserCreate(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]+$")]
    email: EmailStr
    name: Annotated[str, Field(min_length=2, max_length=50)]
    country: Annotated[str, Field(min_length=2, max_length=50)]
    gender: Annotated[str, Field(pattern="^(male|female|other)$")]
    password: Annotated[str, Field(min_length=8, max_length=128)]
    phone: Optional[str] = None  # Optional on creation
    profile_photo_url: Optional[str] = None  # Optional on creation

class UserUpdate(BaseModel):
    name: Optional[Annotated[str, Field(min_length=2, max_length=50)]]
    country: Optional[Annotated[str, Field(min_length=2, max_length=50)]]
    gender: Optional[Annotated[str, Field(pattern="^(male|female|other)$")]]
    phone: Optional[str]
    profile_photo_url: Optional[str]



class UserPublic(BaseModel):
    id: int
    username: str
    name: str
    country: str
    gender: str
    profile_photo_url: Optional[str]
    role: UserRole
    creator_application_status: CreatorApplicationStatus
    status: UserStatus

class UserDetail(UserPublic):
    email: EmailStr
    phone: Optional[str]
    email_verified: bool
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username_or_email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

class UpdateMeRequest(BaseModel):
    # Add any fields user can update
    name: str = None
    country: str = None    
    gender: str = None
    phone: str = None
    profile_photo_url: str = None

class MessageResponse(BaseModel):
    message: str


class AvatarResponse(BaseModel):
    avatar_url: str

