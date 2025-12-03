from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from app.db import models
from app.schemas.user import UserCreate

# Password hashing setup
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash password
def hash_password(password: str) -> str:
    return pwd.hash(password)

# Get user by username
async def get_user(username: str, db: AsyncSession):
    query = select(models.User).where(models.User.username == username)
    result = await db.execute(query)
    return result.scalars().first()

# Create a new user
async def create_user(user: UserCreate, db: AsyncSession):
    hashed_password = hash_password(user.password)  # now fixed
    new_user = models.User(
        username=user.username,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# Authenticate user
async def authenticate(username: str, password: str, db: AsyncSession):
    user = await get_user(username, db)
    if not user:
        return None
    if not pwd.verify(password, user.hashed_password):
        return None
    return user
