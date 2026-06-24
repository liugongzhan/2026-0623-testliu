from typing import Optional, List, Any

from pydantic import BaseModel, ConfigDict


class QuestionCreate(BaseModel):
    course_id: int
    type: str  # single/multi/judge/fill
    content: str
    options: Optional[List[str]] = None
    answer: str
    analysis: Optional[str] = None
    difficulty: int = 1


class QuestionUpdate(BaseModel):
    type: Optional[str] = None
    content: Optional[str] = None
    options: Optional[List[str]] = None
    answer: Optional[str] = None
    analysis: Optional[str] = None
    difficulty: Optional[int] = None


class QuestionResponse(BaseModel):
    id: int
    course_id: int
    type: str
    content: str
    options: Optional[Any] = None
    answer: Optional[str] = None  # 仅教师/管理员可见
    analysis: Optional[str] = None
    difficulty: int

    model_config = ConfigDict(from_attributes=True)


class QuestionStudentResponse(BaseModel):
    """学生视角 — 不返回答案"""
    id: int
    course_id: int
    type: str
    content: str
    options: Optional[Any] = None
    difficulty: int

    model_config = ConfigDict(from_attributes=True)
