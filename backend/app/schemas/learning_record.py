from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class LearningRecordCreate(BaseModel):
    course_id: int
    chapter_id: int
    progress: float = 0
    last_position: float = 0
    completed: bool = False


class LearningRecordUpdate(BaseModel):
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
