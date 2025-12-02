# app/deps/dependencies.py
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.crud.user import get_user
from app.auth.jwt_handler import decode_token
from app.schemas.user import TokenPayload


# Get current user from JWT token
async def get_current_user(token: str = Depends(lambda: None), db: AsyncSession = Depends(get_db)):
    payload = decode_token(token)
    if not payload or not getattr(payload, "username", None):
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await get_user(payload.username, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Role-based access dependency
def require_role(role: str):
    async def checker(user=Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user

    return checker
