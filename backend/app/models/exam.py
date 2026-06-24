from sqlalchemy import Column, BigInteger, String, Integer, DECIMAL, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Exam(Base):
    __tablename__ = "exam"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    course_id = Column(BigInteger, ForeignKey("course.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    duration = Column(Integer, nullable=False, default=60)
    total_score = Column(DECIMAL(5, 1), nullable=False, default=100.0)
    passing_score = Column(DECIMAL(5, 1), nullable=False, default=60.0)
    start_time = Column(DateTime, default=None)
    end_time = Column(DateTime, default=None)
    status = Column(String(20), nullable=False, default="draft", index=True)

    # Relationships
    course = relationship("Course", back_populates="exams")
    exam_records = relationship("ExamRecord", back_populates="exam")
