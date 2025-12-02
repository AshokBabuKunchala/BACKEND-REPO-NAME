from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from app.db import models
from app.schemas.user import UserCreate


pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user(username: str, db: AsyncSession):
    query = select(models.User).where(models.User.username == username)
    result = await db.execute(query)
    return result.scalars().first()


async def create_user(user: UserCreate, db: AsyncSession):
    hashed = pwd.hash(user.password)
    new_user = models.User(
        username=user.username,
        hashed_password=hashed,
        role=user.role
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def authenticate(username: str, password: str, db: AsyncSession):
    user = await get_user(username, db)
    if not user:
        return None
    if not pwd.verify(password, user.hashed_password):
        return None
    return user
