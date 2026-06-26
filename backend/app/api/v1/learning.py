"""学习记录 API"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.user import SysUser
from app.models.course import Course
from app.models.chapter import Chapter
from app.models.learning_record import LearningRecord
from app.schemas.learning_record import (
    LearningRecordUpdate,
    LearningRecordResponse,
    CourseProgressResponse,
    ChapterProgressItem,
    LearningHistoryItem,
)
from app.api.deps import get_current_active_user

router = APIRouter()


@router.post("/progress", response_model=LearningRecordResponse)
def save_progress(
    course_id: int = Query(...),
    chapter_id: int = Query(...),
    position: float = Query(..., ge=0, description="播放位置（秒）"),
    progress: float = Query(..., ge=0, le=100, description="进度百分比"),
    db: Session = Depends(get_db),
    current_user: SysUser = Depends(get_current_active_user),
):
    """保存/更新学习进度 — 前端定时调用实现断点续播。"""
    # 验证课程和章节存在
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")

    chapter = db.query(Chapter).filter(Chapter.id == chapter_id, Chapter.course_id == course_id).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="章节不存在")

    # 查找或创建记录（按 user_id + chapter_id 唯一）
    record = (
        db.query(LearningRecord)
        .filter(
            LearningRecord.user_id == current_user.id,
            LearningRecord.chapter_id == chapter_id,
        )
        .first()
    )

    if record:
        record.progress = progress
        record.last_position = position
        record.completed = progress >= 100
    else:
        record = LearningRecord(
            user_id=current_user.id,
            course_id=course_id,
            chapter_id=chapter_id,
            progress=progress,
            last_position=position,
            completed=progress >= 100,
        )
        db.add(record)

    db.commit()
    db.refresh(record)
    return record


@router.get("/progress/{course_id}", response_model=CourseProgressResponse)
def get_course_progress(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: SysUser = Depends(get_current_active_user),
):
    """获取用户在某课程中的完整学习进度。"""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")

    # 获取课程所有章节
    chapters = db.query(Chapter).filter(Chapter.course_id == course_id).all()
    # 获取用户在此课程的所有学习记录
    records = (
        db.query(LearningRecord)
        .filter(
            LearningRecord.user_id == current_user.id,
            LearningRecord.course_id == course_id,
        )
        .all()
    )
    record_map = {r.chapter_id: r for r in records}

    chapter_items = []
    completed_count = 0
    last_chapter_id = None
    last_position = 0.0

    for ch in chapters:
        rec = record_map.get(ch.id)
        item = ChapterProgressItem(
            chapter_id=ch.id,
            title=ch.title,
            completed=rec.completed if rec else False,
            progress=rec.progress if rec else 0,
            last_position=rec.last_position if rec else 0,
        )
        chapter_items.append(item)
        if item.completed:
            completed_count += 1
        # 记录最后学习的章节
        if rec and (last_chapter_id is None or rec.last_position > last_position):
            last_chapter_id = ch.id
            last_position = rec.last_position

    total = len(chapters)
    overall = (completed_count / total * 100) if total > 0 else 0

    return CourseProgressResponse(
        course_id=course_id,
        total_chapters=total,
        completed_chapters=completed_count,
        overall_progress=round(overall, 1),
        last_chapter_id=last_chapter_id,
        last_position=last_position,
        chapters=chapter_items,
    )


@router.get("/history", response_model=List[LearningHistoryItem])
def get_learning_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: SysUser = Depends(get_current_active_user),
):
    """获取当前用户的学习历史列表（按最近学习时间倒序）。"""
    records = (
        db.query(LearningRecord)
        .options(
            joinedload(LearningRecord.course),
            joinedload(LearningRecord.chapter),
        )
        .filter(LearningRecord.user_id == current_user.id)
        .order_by(LearningRecord.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return [
        LearningHistoryItem(
            course_id=r.course_id,
            course_title=r.course.title if r.course else "",
            chapter_id=r.chapter_id,
            chapter_title=r.chapter.title if r.chapter else "",
            progress=r.progress,
            last_position=r.last_position,
            completed=r.completed,
            updated_at=r.created_at,
        )
        for r in records
    ]


@router.post("/complete/{chapter_id}", response_model=LearningRecordResponse)
def complete_chapter(
    chapter_id: int,
    course_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: SysUser = Depends(get_current_active_user),
):
    """手动标记章节为已完成。"""
    chapter = db.query(Chapter).filter(
        Chapter.id == chapter_id,
        Chapter.course_id == course_id,
    ).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="章节不存在")

    record = (
        db.query(LearningRecord)
        .filter(
            LearningRecord.user_id == current_user.id,
            LearningRecord.chapter_id == chapter_id,
        )
        .first()
    )

    if record:
        record.completed = True
        record.progress = 100.0
        if chapter.duration:
            record.last_position = float(chapter.duration)
    else:
        record = LearningRecord(
            user_id=current_user.id,
            course_id=course_id,
            chapter_id=chapter_id,
            progress=100.0,
            last_position=float(chapter.duration or 0),
            completed=True,
        )
        db.add(record)

    db.commit()
    db.refresh(record)
    return record
