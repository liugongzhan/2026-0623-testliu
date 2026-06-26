from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class LearningRecordCreate(BaseModel):
    course_id: int
    chapter_id: int
    progress: float = 0
    last_position: float = 0
    completed: bool = False


class LearningRecordUpdate(BaseModel):
    """更新学习进度 — 只需传变更的字段"""
    progress: Optional[float] = None
    last_position: Optional[float] = None
    completed: Optional[bool] = None


class LearningRecordResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    chapter_id: int
    progress: float
    last_position: float
    completed: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CourseProgressResponse(BaseModel):
    """课程学习进度概览"""
    course_id: int
    total_chapters: int
    completed_chapters: int
    overall_progress: float
    last_chapter_id: Optional[int] = None
    last_position: float = 0
    chapters: List["ChapterProgressItem"] = []


class ChapterProgressItem(BaseModel):
    chapter_id: int
    title: str
    completed: bool
    progress: float
    last_position: float

    model_config = ConfigDict(from_attributes=True)


class LearningHistoryItem(BaseModel):
    """学习历史项"""
    course_id: int
    course_title: str
    chapter_id: int
    chapter_title: str
    progress: float
    last_position: float
    completed: bool
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
