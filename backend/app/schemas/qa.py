from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class QACreate(BaseModel):
    chapter_id: int
    question: str


class QAUpdate(BaseModel):
    """教师回答"""
    answer: str


class QAResponse(BaseModel):
    id: int
    user_id: int
    chapter_id: int
    question: str
    answer: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
