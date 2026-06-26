from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class NoteCreate(BaseModel):
    content: str
    timestamp: Optional[int] = None


class NoteUpdate(BaseModel):
    content: Optional[str] = None
    timestamp: Optional[int] = None


class NoteResponse(BaseModel):
    id: int
    user_id: int
    chapter_id: int
    content: str
    timestamp: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
