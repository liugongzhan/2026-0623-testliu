from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import SysUser
from app.schemas.user import UserResponse, UserUpdate
from app.api.deps import get_current_active_user, require_role

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
def list_users(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db),
    current_user: SysUser = Depends(require_role("admin")),
):
    """获取用户列表（仅管理员）。"""
    offset = (page - 1) * page_size
    users = db.query(SysUser).offset(offset).limit(page_size).all()
    return [UserResponse.model_validate(u) for u in users]


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: SysUser = Depends(get_current_active_user),
):
    """获取指定用户信息。"""
    user = db.query(SysUser).filter(SysUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    return UserResponse.model_validate(user)


@router.put("/me", response_model=UserResponse)
def update_me(
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: SysUser = Depends(get_current_active_user),
):
    """更新当前用户自己的信息。"""
    if data.nickname is not None:
        current_user.nickname = data.nickname
    if data.email is not None:
        # 检查邮箱是否被其他用户使用
        existing = db.query(SysUser).filter(
            SysUser.email == data.email, SysUser.id != current_user.id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="邮箱已被其他用户使用",
            )
        current_user.email = data.email
    if data.avatar is not None:
        current_user.avatar = data.avatar

    db.commit()
    db.refresh(current_user)
    return UserResponse.model_validate(current_user)


@router.put("/{user_id}/status", response_model=UserResponse)
def update_user_status(
    user_id: int,
    status_value: int = Query(..., description="状态: 1=正常 0=禁用"),
    db: Session = Depends(get_db),
    current_user: SysUser = Depends(require_role("admin")),
):
    """修改用户状态（仅管理员）。"""
    user = db.query(SysUser).filter(SysUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    if user.role == "admin" and status_value == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能禁用管理员账户",
        )

    user.status = status_value
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)
