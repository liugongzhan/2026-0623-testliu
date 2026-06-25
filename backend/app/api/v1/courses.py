"""课程管理 API"""
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import SysUser
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse, CourseListResponse
from app.api.deps import get_current_active_user, require_role
from app.services.course import CourseService

router = APIRouter()


@router.get("/", response_model=CourseListResponse)
def list_courses(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    category_id: Optional[int] = Query(None, description="分类ID"),
    status: Optional[str] = Query("published", description="课程状态"),
    teacher_id: Optional[int] = Query(None, description="讲师ID"),
    db: Session = Depends(get_db),
):
    """课程列表（公开），支持分页、搜索、分类筛选。"""
    result = CourseService.list_courses(
        db=db,
        page=page,
        page_size=page_size,
        keyword=keyword,
        category_id=category_id,
        status=status,
        teacher_id=teacher_id,
    )
    return {"total": result["total"], "items": result["items"]}


@router.get("/my", response_model=CourseListResponse)
def list_my_courses(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: SysUser = Depends(require_role("teacher", "admin")),
):
    """我的课程（讲师视角），返回所有状态的课程。"""
    result = CourseService.list_courses(
        db=db,
        page=page,
        page_size=page_size,
        status=None,
        teacher_id=current_user.id,
    )
    return {"total": result["total"], "items": result["items"]}


@router.post("/", response_model=CourseResponse, status_code=201)
def create_course(
    data: CourseCreate,
    db: Session = Depends(get_db),
    current_user: SysUser = Depends(require_role("teacher", "admin")),
):
    """创建课程（教师/管理员）。"""
    course = CourseService.create_course(db, data, teacher_id=current_user.id)
    return course


@router.get("/{course_id}", response_model=CourseResponse)
def get_course(
    course_id: int,
    db: Session = Depends(get_db),
):
    """课程详情（公开）。"""
    course = CourseService.get_course(db, course_id)
    return course


@router.put("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int,
    data: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: SysUser = Depends(get_current_active_user),
):
    """更新课程（讲师本人或管理员）。"""
    course = CourseService.update_course(db, course_id, data, current_user)
    return course


@router.delete("/{course_id}")
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: SysUser = Depends(get_current_active_user),
):
    """删除课程（讲师本人或管理员）。"""
    CourseService.delete_course(db, course_id, current_user)
    return {"message": "课程已删除"}
