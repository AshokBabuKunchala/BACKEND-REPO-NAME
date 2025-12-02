from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.crud.user import authenticate, create_user, get_user
from app.schemas.user import UserCreate, Token
from app.auth.jwt_handler import create_access_token

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await authenticate(form.username, form.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"username": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register")
async def register(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    existing = await get_user(user.username, db)
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    return await create_user(user, db)
