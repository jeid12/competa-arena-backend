from sqlmodel import Session, select
from datetime import datetime, timedelta
from fastapi import HTTPException
from utils.otp import generate_otp
from utils.email import send_otp_email
from models.users import User
from schemas.user_schemas import UserCreate
from utils.password import hash_password, verify_password
from utils.image import upload_profile_photo
from utils.email import send_password_reset_email

def create_user(user_in: UserCreate, db: Session) -> User:
    hashed_pw = hash_password(user_in.password)
    avatar_url = None
    if user_in.profile_photo_url:
        avatar_url = upload_profile_photo(user_in.profile_photo_url, public_id=f"user_{user_in.username}")

    otp = generate_otp()
    expiry = datetime.utcnow() + timedelta(minutes=10)
    user = User(
        username=user_in.username,
        email=user_in.email,
        name=user_in.name,
        country=user_in.country,
        gender=user_in.gender,
        phone=user_in.phone,
        password=hashed_pw,
        profile_photo_url=avatar_url,
        otp_code=otp,
        otp_expiry=expiry,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    send_otp_email(user.email, otp)
    return user

def verify_otp(user: User, otp_from_user: str, db: Session):
    if user.email_verified:
        raise HTTPException(400, "Email already verified!")
    if not user.otp_code or not user.otp_expiry:
        raise HTTPException(400, "No OTP pending for user")
    if datetime.utcnow() > user.otp_expiry:
        raise HTTPException(400, "OTP expired, please request a new one")
    if user.otp_code != otp_from_user:
        raise HTTPException(400, "Invalid OTP")
    user.email_verified = True
    user.otp_code = None
    user.otp_expiry = None
    db.add(user)
    db.commit()
    db.refresh(user)
    return True

def resend_otp(user: User, db: Session):
    if user.email_verified:
        raise HTTPException(400, "Email already verified!")
    otp = generate_otp()
    expiry = datetime.utcnow() + timedelta(minutes=10)
    user.otp_code = otp
    user.otp_expiry = expiry
    db.add(user)
    db.commit()
    db.refresh(user)
    send_otp_email(user.email, otp)
    return True

def send_password_reset_otp(email: str, db: Session):
    user = db.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(404, "User not found")
    otp = generate_otp()
    expiry = datetime.utcnow() + timedelta(minutes=10)
    user.reset_otp = otp
    user.reset_otp_expiry = expiry
    db.add(user)
    db.commit()
    send_password_reset_email(user.email, otp)
    return True

def reset_password(email: str, otp: str, new_password: str, db: Session):
    user = db.exec(select(User).where(User.email == email)).first()
    if not user or not user.reset_otp or not user.reset_otp_expiry:
        raise HTTPException(400, "No password reset requested")
    if user.reset_otp != otp or datetime.utcnow() > user.reset_otp_expiry:
        raise HTTPException(400, "Invalid or expired OTP")
    user.password = hash_password(new_password)
    user.reset_otp = None
    user.reset_otp_expiry = None
    db.add(user)
    db.commit()
    return True

def get_me(user: User):
    return user

def update_me(user: User, update_data: dict, db: Session):
    for k, v in update_data.items():
        setattr(user, k, v)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def change_password(user: User, old_password: str, new_password: str, db: Session):
    if not verify_password(old_password, user.password):
        raise HTTPException(400, "Old password incorrect")
    user.password = hash_password(new_password)
    db.add(user)
    db.commit()
    return True