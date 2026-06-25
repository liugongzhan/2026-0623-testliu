"""章节管理 API"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.course import Course
from app.models.chapter import Chapter
from app.models.user import SysUser
from app.schemas.chapter import ChapterCreate, ChapterUpdate, ChapterResponse, ChapterTreeResponse
from app.api.deps import get_current_active_user, require_role

router = APIRouter()


def _build_chapter_tree(chapters: List[Chapter], parent_id: int | None = None) -> list:
    """递归构建章节目录树"""
    tree = []
    children = [c for c in chapters if c.parent_id == parent_id]
    children.sort(key=lambda c: c.sort_order)
    for ch in children:
        node = ChapterTreeResponse.model_validate(ch)
        node.children = _build_chapter_tree(chapters, ch.id)
        tree.append(node)
    return tree


@router.get("/courses/{course_id}/chapters", response_model=List[ChapterTreeResponse])
def list_chapters(
    course_id: int,
    db: Session = Depends(get_db),
):
    """获取课程章节列表（树形结构）。"""
    # 验证课程存在
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="课程不存在")

    chapters = (
        db.query(Chapter)
        .filter(Chapter.course_id == course_id)
        .order_by(Chapter.sort_order)
        .all()
    )
    return _build_chapter_tree(chapters)


@router.post("/courses/{course_id}/chapters", response_model=ChapterResponse, status_code=201)
def create_chapter(
    course_id: int,
    data: ChapterCreate,
    db: Session = Depends(get_db),
    current_user: SysUser = Depends(require_role("teacher", "admin")),
):
    """创建章节（教师/管理员）。"""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="课程不存在")

    # 权限检查
    if current_user.role != "admin" and course.teacher_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权操作此课程")

    # 如果设置了 parent_id，验证父章节属于同一课程
    if data.parent_id:
        parent = db.query(Chapter).filter(Chapter.id == data.parent_id).first()
        if not parent or parent.course_id != course_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="父章节无效")

    chapter = Chapter(
        course_id=course_id,
        title=data.title,
        sort_order=data.sort_order,
        parent_id=data.parent_id,
        video_url=data.video_url,
        duration=data.duration,
        is_free=data.is_free,
    )
    db.add(chapter)
    db.commit()
    db.refresh(chapter)
    return chapter


@router.put("/chapters/{chapter_id}", response_model=ChapterResponse)
def update_chapter(
    chapter_id: int,
    data: ChapterUpdate,
    db: Session = Depends(get_db),
    current_user: SysUser = Depends(require_role("teacher", "admin")),
):
    """更新章节。"""
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="章节不存在")

    # 权限检查
    course = db.query(Course).filter(Course.id == chapter.course_id).first()
    if current_user.role != "admin" and course.teacher_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权操作")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(chapter, field, value)

    db.commit()
    db.refresh(chapter)
    return chapter


@router.delete("/chapters/{chapter_id}")
def delete_chapter(
    chapter_id: int,
    db: Session = Depends(get_db),
    current_user: SysUser = Depends(require_role("teacher", "admin")),
):
    """删除章节（级联删除子章节）。"""
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="章节不存在")

    course = db.query(Course).filter(Course.id == chapter.course_id).first()
    if current_user.role != "admin" and course.teacher_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权操作")

    # 级联删除子章节
    def _delete_children(parent_id: int):
        children = db.query(Chapter).filter(Chapter.parent_id == parent_id).all()
        for child in children:
            _delete_children(child.id)
            db.delete(child)

    _delete_children(chapter.id)
    db.delete(chapter)
    db.commit()
    return {"message": "章节已删除"}


@router.put("/chapters/{chapter_id}/sort")
def sort_chapter(
    chapter_id: int,
    sort_order: int = 0,
    db: Session = Depends(get_db),
    current_user: SysUser = Depends(require_role("teacher", "admin")),
):
    """调整章节排序。"""
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="章节不存在")

    chapter.sort_order = sort_order
    db.commit()
    return {"message": "排序已更新"}
