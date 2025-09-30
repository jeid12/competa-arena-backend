from fastapi import HTTPException
from sqlmodel import Session, select
from models.users import User

def list_creator_applications(db: Session):
    return db.exec(select(User).where(User.creator_application_status == "pending")).all()

def approve_creator(username: str, db: Session):
    user = db.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(404, "User not found")
    if user.creator_application_status != "pending":
        raise HTTPException(400, "User is not pending approval")
    user.creator_application_status = "approved"
    user.role = "creator"
    db.add(user)
    db.commit()
    db.refresh(user)
    return True

def assign_role(username: str, new_role: str, db: Session):
    user = db.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(404, "User not found")
    user.role = new_role
    db.add(user)
    db.commit()
    db.refresh(user)
    return True

def suspend_user(username: str, db: Session):
    user = db.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(404, "User not found")
    user.status = "suspended"
    db.add(user)
    db.commit()
    db.refresh(user)
    return True

def reactivate_user(username: str, db: Session):
    user = db.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(404, "User not found")
    user.status = "active"
    db.add(user)
    db.commit()
    db.refresh(user)
    return True

def block_user(username: str, db: Session):
    user = db.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(404, "User not found")
    user.status = "blocked"
    db.add(user)
    db.commit()
    db.refresh(user)
    return True

# get all users - for admin dashboard
def get_all_users(db: Session):
    user=db.exec(select(User)).all()
    if not user:
        raise HTTPException(404, "No users found")
    return user
