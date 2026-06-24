from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import SysUser
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.user import UserCreate, UserResponse, TokenResponse


class AuthService:
    """认证相关的业务逻辑。"""

    @staticmethod
    def register_user(db: Session, data: UserCreate) -> TokenResponse:
        """注册新用户并返回 token。"""
        # 检查用户名唯一性
        if db.query(SysUser).filter(SysUser.username == data.username).first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="用户名已存在",
            )

        # 检查邮箱唯一性
        if data.email and db.query(SysUser).filter(SysUser.email == data.email).first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="邮箱已被注册",
            )

        user = SysUser(
            username=data.username,
            password=hash_password(data.password),
            nickname=data.nickname or data.username,
            email=data.email,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        access_token = create_access_token(data={"sub": str(user.id)})

        return TokenResponse(
            access_token=access_token,
            user=UserResponse.model_validate(user),
        )

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> SysUser:
        """验证用户名密码，返回用户对象。"""
        user = db.query(SysUser).filter(SysUser.username == username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
            )
        if not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
            )
        if user.status != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="账户已被禁用",
            )
        return user

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> SysUser:
        """根据 ID 获取用户。"""
        user = db.query(SysUser).filter(SysUser.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
        return user
