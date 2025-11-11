from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """
    User 기본 스키마
    """
    email: EmailStr
    username: str


class UserCreate(UserBase):
    """
    User 생성 스키마
    """
    password: str


class UserUpdate(BaseModel):
    """
    User 업데이트 스키마
    """
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    """
    User 응답 스키마
    """
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
