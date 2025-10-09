from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status, Body, Request
from sqlmodel import Session, select
from config.db import get_session
from schemas.user_schemas import AvatarResponse, ChangePasswordRequest, ForgotPasswordRequest, PublicUserProfile, ResetPasswordRequest, UpdateMeRequest, UserCreate, UserDetail,MessageResponse
from models.users import User
from services.user_service import change_password, create_user, get_me, reset_password, send_password_reset_otp, update_avatar, update_me, verify_otp, resend_otp , get_public_profile 
from rate_limiting import limiter
from utils.auth import decode_access_token, get_current_user
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()
router = APIRouter()


@router.get("/validate-token")
def validate_token(request: Request, db: Session = Depends(get_session)):
    """
    Validates the JWT access token and returns user info:
    {
        "userId": str,
        "role": str
    }
    """
    auth_header = request.headers.get("Authorization")
    print("Authorization header:", auth_header)
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = auth_header.split(" ")[1]

    # Decode access token
    payload = decode_access_token(token)
    print("Decoded token payload:", payload)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id_raw = payload.get("sub")
    role_from_token = payload.get("role")

    print("User ID from token (raw):", user_id_raw)

    if user_id_raw is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    # Try to coerce numeric-looking IDs to int, otherwise use as-is (handles string/uuid ids)
    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError):
        user_id = user_id_raw

    # Fetch user from DB safely using the coerced id
    db_user = db.exec(select(User).where(User.id == user_id)).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="User not found")

    # Optional: verify role from token matches DB role
    if db_user.role != role_from_token:
        raise HTTPException(status_code=401, detail="Token role mismatch")

    return {
        "userId": str(db_user.id),
        "role": db_user.role
    }
