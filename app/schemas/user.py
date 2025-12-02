from pydantic import BaseModel
from typing import Optional

# Base model for user input
class UserBase(BaseModel):
    username: str

# Model for creating a new user
class UserCreate(UserBase):
    password: str
    role: Optional[str] = "user"

# Model for reading user data from DB
class UserRead(UserBase):
    id: int
    is_active: bool
    role: str

    class Config:
        orm_mode = True  # Important for ORM objects like SQLAlchemy

# Model for API response (can be same as UserRead or customized)
class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    is_active: bool

    class Config:
        orm_mode = True

# Token models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[str]
    username: Optional[str]
    role: Optional[str]
