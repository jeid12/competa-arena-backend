from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status, Body, Request
from sqlmodel import Session, select
from config.db import get_session
from schemas.user_schemas import AvatarResponse, ChangePasswordRequest, ForgotPasswordRequest, PublicUserProfile, ResetPasswordRequest, UpdateMeRequest, UserCreate, UserDetail,MessageResponse
from models.users import User
from services.user_service import change_password, create_user, get_me, reset_password, send_password_reset_otp, update_avatar, update_me, verify_otp, resend_otp , get_public_profile 
from rate_limiting import limiter
from utils.auth import get_current_user
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()
router = APIRouter()

@router.post("/register", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/hour")
def register_user(user_in: UserCreate, db: Session = Depends(get_session), request: Request = None):
    user = create_user(user_in, db)
    return {"message": "User registered successfully Please verify your email"}

@router.post("/verify-email")
@limiter.limit("2/hour")
def verify_email(username: str = Body(...), otp: str = Body(...), db: Session = Depends(get_session), request: Request = None):
    user = db.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(404, "User not found")
    verify_otp(user, otp, db)
    return {"message": "Email verified successfully"}

@router.post("/resend-otp")
@limiter.limit("1/hour")
def resend_otp_endpoint(username: str = Body(...), db: Session = Depends(get_session), request: Request = None):
    user = db.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(404, "User not found")
    resend_otp(user, db)
    return {"message": "OTP resent"}

@router.post("/forgot-password")
def forgot_password(
    req: ForgotPasswordRequest,
    db: Session = Depends(get_session)
):
    send_password_reset_otp(req.email, db)
    return {"message": "Reset OTP sent"}

@router.post("/reset-password")
def reset_password_endpoint(
    req: ResetPasswordRequest,
    db: Session = Depends(get_session)
):
    reset_password(req.email, req.otp, req.new_password, db)
    return {"message": "Password reset successful"}

@router.get("/me", response_model=UserDetail, dependencies=[Depends(security)])
def me(
    user=Depends(get_current_user)
):
    return get_me(user)

@router.put("/me", response_model=UserDetail,dependencies=[Depends(security)] )
def update_me_endpoint(
    update: UpdateMeRequest,
    db: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    return update_me(user, update.dict(exclude_unset=True), db)

@router.put("/me/password",dependencies=[Depends(security)])
def change_password_endpoint(
    req: ChangePasswordRequest,
    db: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    change_password(user, req.old_password, req.new_password, db)
    return {"message": "Password changed successfully"}


@router.post("/me/avatar", response_model=AvatarResponse, status_code=status.HTTP_200_OK , dependencies = [Depends(security)])
async def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    avatar_url = update_avatar(user, file.file, db)
    return AvatarResponse(avatar_url=avatar_url)

@router.get("/{username}", response_model=PublicUserProfile)
def public_profile(username: str, db: Session = Depends(get_session)):
    profile = get_public_profile(username, db)
    return profile