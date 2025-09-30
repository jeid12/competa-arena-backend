from utils.auth import create_access_token, create_refresh_token
from sqlmodel import Session, select
from fastapi import HTTPException
from models.users import User
from utils.password import verify_password

def authenticate_user(username_or_email: str, password: str, db: Session):
    user = db.exec(
        select(User).where(
            (User.username == username_or_email) | (User.email == username_or_email)
        )
    ).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(401, "Incorrect username/email or password")
    if not user.email_verified:
        raise HTTPException(403, "Email is not verified")
    if user.status != "active":
        raise HTTPException(403, f"Account is {user.status}")

    from datetime import datetime
    user.last_login = datetime.utcnow()
    db.add(user)
    db.commit()
    db.refresh(user)

    claims = {"sub": str(user.id), "username": user.username, "role": user.role}
    access_token = create_access_token(claims)
    refresh_token = create_refresh_token(claims)
    return access_token, refresh_token

def apply_creator(user: User, db: Session):
    if user.role != "user":
        raise HTTPException(403, "Only users can apply for creator role")
    if user.creator_application_status == "pending":
        raise HTTPException(400, "Creator application already pending")
    if user.creator_application_status == "approved":
        raise HTTPException(400, "Already approved as creator")
    user.creator_application_status = "pending"
    db.add(user)
    db.commit()
    db.refresh(user)
    return True