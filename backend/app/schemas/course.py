from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None
    cover_image: Optional[str] = None
    category_id: Optional[int] = None
    price: Decimal = Decimal("0.00")
    status: str = "draft"


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    cover_image: Optional[str] = None
    category_id: Optional[int] = None
    price: Optional[Decimal] = None
    status: Optional[str] = None


class CourseResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    cover_image: Optional[str] = None
    category_id: Optional[int] = None
    teacher_id: int
    price: Decimal
    status: str
    student_count: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CourseListResponse(BaseModel):
    total: int
    items: List[CourseResponse]
