from fastapi import APIRouter, Depends, status, Response, Request, HTTPException
from sqlmodel import Session
from config.db import get_session
from schemas.user_schemas import UserLogin, TokenResponse
from services.user_login import apply_creator, authenticate_user
from utils.auth import decode_refresh_token, create_access_token, create_refresh_token, get_current_user
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()
router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(
    login_in: UserLogin,
    response: Response,
    db: Session = Depends(get_session),
):
    access_token, refresh_token = authenticate_user(login_in.username_or_email, login_in.password, db)
    # Set HTTP-only refresh token cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=7*24*60*60  # 7 days
    )
    return TokenResponse(access_token=access_token)

@router.post("/refresh-token", response_model=TokenResponse)
def refresh_token(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(401, "Refresh token missing")
    payload = decode_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(401, "Invalid or expired refresh token")

    user_claims = {
        "sub": payload["sub"],
        "username": payload["username"],
        "role": payload["role"]
    }
    access_token = create_access_token(user_claims)
    
    new_refresh_token = create_refresh_token(user_claims)
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=7*24*60*60
    )
    return TokenResponse(access_token=access_token)

@router.post("/me/apply-creator", status_code=status.HTTP_200_OK, dependencies=[Depends(security)])
def apply_creator_endpoint(
    db: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    apply_creator(user, db)
    return {"message": "Creator application submitted and is now pending admin review."}


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(response: Response):
    # Remove refresh token cookie by setting it to empty and expiring it
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=True,
        samesite="lax",
        path="/"
    )
    return {"message": "Logged out successfully"}