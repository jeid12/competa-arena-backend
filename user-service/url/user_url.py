from fastapi import APIRouter
from controllers.user_controller import router as user_router
from controllers.user_login_controller import router as user_login_router
from controllers.admin_controller import router as admin_router

api_router = APIRouter()
api_router.include_router(user_router, prefix="/api/auth", tags=["Authentication"])
api_router.include_router(user_login_router, prefix="/api/auth", tags=["Authentication"])
api_router.include_router(admin_router, prefix="/api/admin", tags=["Admin "])