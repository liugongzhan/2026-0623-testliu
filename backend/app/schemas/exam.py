from datetime import datetime
from decimal import Decimal
from typing import Optional, Dict

from pydantic import BaseModel, ConfigDict


class ExamCreate(BaseModel):
    course_id: int
    title: str
    duration: int = 60
    total_score: Decimal = Decimal("100.0")
    passing_score: Decimal = Decimal("60.0")
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class ExamUpdate(BaseModel):
    title: Optional[str] = None
    duration: Optional[int] = None
    total_score: Optional[Decimal] = None
    passing_score: Optional[Decimal] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[str] = None


class ExamResponse(BaseModel):
    id: int
    course_id: int
    title: str
    duration: int
    total_score: Decimal
    passing_score: Decimal
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: str

    model_config = ConfigDict(from_attributes=True)


class ExamSubmit(BaseModel):
    """学生提交考试答案"""
    answers: Dict[int, str]  # { question_id: answer }
