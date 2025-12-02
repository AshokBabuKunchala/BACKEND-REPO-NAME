# app/routers/users.py
from fastapi import APIRouter, Depends
from app.deps.dependencies import require_role, get_current_user
from app.schemas.user import UserResponse

router = APIRouter(prefix="/api/users", tags=["Users"])


# Admin-only route
@router.get("/admin")
async def admin_dashboard(user=Depends(require_role("admin"))):
    return {"message": f"Hello, {user.username}. You are an admin."}


# Current user info route
@router.get("/me", response_model=UserResponse)
async def read_current_user(user=Depends(get_current_user)):
    return user
