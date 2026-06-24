from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    """注册用户请求"""
    username: str
    password: str
    nickname: Optional[str] = None
    email: Optional[EmailStr] = None


class UserLogin(BaseModel):
    """登录请求 (JSON 格式)"""
    username: str
    password: str


class UserResponse(BaseModel):
    """用户信息响应"""
    id: int
    username: str
    nickname: Optional[str] = None
    email: Optional[str] = None
    avatar: Optional[str] = None
    role: str
    status: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    """更新用户信息请求"""
    nickname: Optional[str] = None
    email: Optional[EmailStr] = None
    avatar: Optional[str] = None


class TokenResponse(BaseModel):
    """登录/注册成功后返回的令牌"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
