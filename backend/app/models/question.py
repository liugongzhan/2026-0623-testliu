from sqlalchemy import Column, Integer, String, Text, JSON, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("course.id", ondelete="CASCADE"), nullable=False, index=True)
    type = Column(String(20), nullable=False, index=True, comment="题型: single/multi/judge/fill")
    content = Column(Text, nullable=False)
    options = Column(JSON, default=None)
    answer = Column(Text, nullable=False)
    analysis = Column(Text, default=None)
    difficulty = Column(SmallInteger, nullable=False, default=1)

    # Relationships
    course = relationship("Course", back_populates="questions")
