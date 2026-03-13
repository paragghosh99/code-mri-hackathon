from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# What client sends
class TaskCreate(BaseModel):
    title: str
    description: str

# What client receives
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    is_done: bool

    class Config:
        from_attributes = True

# UPDATE needs optional fields
# Optional fields → enables partial updates
# Presence ≠ overwrite unless explicitly sent
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_done: Optional[bool] = None


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"