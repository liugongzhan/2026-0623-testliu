from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class ChapterCreate(BaseModel):
    course_id: int
    title: str
    sort_order: int = 0
    parent_id: Optional[int] = None
    video_url: Optional[str] = None
    duration: int = 0
    is_free: bool = False


class ChapterUpdate(BaseModel):
    title: Optional[str] = None
    sort_order: Optional[int] = None
    parent_id: Optional[int] = None
    video_url: Optional[str] = None
    duration: Optional[int] = None
    is_free: Optional[bool] = None


class ChapterResponse(BaseModel):
    id: int
    course_id: int
    title: str
    sort_order: int
    parent_id: Optional[int] = None
    video_url: Optional[str] = None
    duration: int
    is_free: bool
    children: List["ChapterResponse"] = []

    model_config = ConfigDict(from_attributes=True)


class ChapterTreeResponse(BaseModel):
    """课程章节树形结构"""
    id: int
    course_id: int
    title: str
    sort_order: int
    parent_id: Optional[int] = None
    duration: int
    is_free: bool
    children: List[ChapterTreeResponse] = []

    model_config = ConfigDict(from_attributes=True)
