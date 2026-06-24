from datetime import datetime
from decimal import Decimal
from typing import Optional, Any

from pydantic import BaseModel, ConfigDict


class ExamRecordResponse(BaseModel):
    id: int
    exam_id: int
    user_id: int
    score: Optional[Decimal] = None
    answers: Optional[Any] = None
    start_time: datetime
    submit_time: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
