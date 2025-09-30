from fastapi import APIRouter, Depends, Body
from sqlmodel import Session
from config.db import get_session
from services.admin_service import (
    approve_creator,
    get_all_users,
    list_creator_applications,
    assign_role,
    suspend_user,
    reactivate_user,
    block_user
)
from utils.auth import require_admin
from schemas.user_schemas import PublicUserProfile
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

router = APIRouter()

@router.get("/users/creator-applications", response_model=list[PublicUserProfile], dependencies=[Depends(security)])
def get_creator_applications(
    db: Session = Depends(get_session),
    admin=Depends(require_admin)
):
    users = list_creator_applications(db)
    return [PublicUserProfile(**{
        "username": u.username,
        "name": u.name,
        "country": u.country,
        "gender": u.gender,
        "profile_photo_url": u.profile_photo_url,
        "role": u.role,
        "creator_application_status": u.creator_application_status,
        "status": u.status
    }) for u in users]

@router.put("/users/{username}/role", dependencies=[Depends(security)])
def put_role(
    username: str,
    new_role: str = Body(...),
    db: Session = Depends(get_session),
    admin=Depends(require_admin)
):
    assign_role(username, new_role, db)
    return {"message": f"Role for {username} set to {new_role}"}

@router.put("/users/{username}/suspend", dependencies=[Depends(security)])
def put_suspend(
    username: str,
    db: Session = Depends(get_session),
    admin=Depends(require_admin)
):
    suspend_user(username, db)
    return {"message": f"User {username} suspended"}

@router.put("/users/{username}/reactivate", dependencies=[Depends(security)])
def put_reactivate(
    username: str,
    db: Session = Depends(get_session),
    admin=Depends(require_admin)
):
    reactivate_user(username, db)
    return {"message": f"User {username} reactivated"}

@router.put("/users/{username}/block", dependencies=[Depends(security)])
def put_block(
    username: str,
    db: Session = Depends(get_session),
    admin=Depends(require_admin)
):
    block_user(username, db)
    return {"message": f"User {username} blocked"}

@router.get("/users", response_model=list[PublicUserProfile], dependencies=[Depends(security)])
def getallusers(
    db: Session = Depends(get_session),
    admin=Depends(require_admin)
):
    users = get_all_users(db)
    return [PublicUserProfile(**{
        "username": u.username,
        "name": u.name,
        "country": u.country,
        "gender": u.gender,
        "profile_photo_url": u.profile_photo_url,
        "role": u.role,
        "creator_application_status": u.creator_application_status,
        "status": u.status,
        "count": len(users)
    }) for u in users]

@router.put("/users/{username}/approve", dependencies=[Depends(security)])
def approvecreator(
    username: str,
    db: Session = Depends(get_session),
    admin=Depends(require_admin)
):
    
    approve_creator(username, db)
    return {"message": f"User {username} approved as creator"}